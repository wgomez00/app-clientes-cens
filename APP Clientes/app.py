from flask import Flask, render_template, request, jsonify, send_file
import os, io, re
from openpyxl import load_workbook

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "app", "templates"), static_folder=os.path.join(BASE_DIR, "app", "static"))
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

censo_lookup = {}
MANUAL_CONFIRMED = {
    "1935920": {
        "municipio": "CUCUTA",
        "cuadrante": "",
        "longitud": "",
        "latitud": "",
        "potencia": "35",
        "farola": "1553529",
        "trafo": "",
        "tecnologia": "LED",
    }
}

municipio_contracto = {}
template_headers = []

# Mapeos confirmados manualmente por el usuario
KNOWN_STICKERS_BY_NAME = {"p1.jpg":"1902173","p2.jpg":"1903903","p3.jpg":"1913922","p4.jpg":"1932636","p5.jpg":"1917445","p7.jpg":"1915660","p8.jpg":"1910410","p9.jpg":"1915645","p11.jpg":"1924068","p12.jpg":"1903289","p14.jpg":"1915650","p16.jpg":"1915687","p17.jpg":"1914630","p18.jpg":"1914094","p6.jpg":"1935920","p10.jpg":"1901142"}


def recognize_sticker(image_path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
        import pytesseract
        tesseract_path = r"C:\Users\Wgomezc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        image = Image.open(image_path)
        width, height = image.size
        regions = [image, image.crop((0, int(height*.20), width, int(height*.80))), image.crop((int(width*.15), int(height*.25), int(width*.85), int(height*.75)))]
        found = set()
        for region in regions:
            region = region.resize((region.width*2, region.height*2))
            gray = ImageOps.autocontrast(region.convert("L"))
            gray = ImageEnhance.Contrast(gray).enhance(2.5)
            text = pytesseract.image_to_string(gray, lang="eng", config="--psm 11")
            found.update(re.findall(r"(?<!\d)\d{6,7}(?!\d)", text))
        valid = found.intersection(set(censo_lookup.keys()))
        return sorted(valid, key=len, reverse=True)[0] if valid else ""
    except Exception:
        return ""
EXCLUDED_POINTS = {"p13.jpg", "p15.jpg"}

def recognize_transformador(image_path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
        import pytesseract
        tesseract_path = r"C:\Users\Wgomezc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        image = Image.open(image_path)
        width, height = image.size
        region = image.crop((0, int(height*.18), width, int(height*.75)))
        region = region.resize((region.width*2, region.height*2))
        text = pytesseract.image_to_string(ImageOps.autocontrast(region.convert("L")), lang="eng", config="--psm 11")
        matches=re.findall(r"(?i)[0-9]+T[0-9]+",text)
        return matches[0].upper() if matches else ""
    except Exception:
        return ""

def recognize_location(image_path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
        import pytesseract
        tesseract_path = r"C:\Users\Wgomezc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        image = Image.open(image_path)
        width, height = image.size
        region = image.crop((0, int(height*.55), width, height))
        region = region.resize((region.width*2, region.height*2))
        gray = ImageOps.autocontrast(region.convert("L"))
        gray = ImageEnhance.Contrast(gray).enhance(2)
        text = pytesseract.image_to_string(gray, lang="eng", config="--psm 11")
        address_markers = re.compile(r"(?i).*(?:carrera|carr|calle|av(?:enida)?|diagonal|transversal|trv|tv|cr[.]|cl[.]|mz|manzana|barrio|vereda).*")
        for line in text.splitlines():
            line = re.sub(r"\s+", " ", line).strip(" ,.-")
            if address_markers.match(line) and len(line) >= 5:
                return line[:120]
        return ""
    except Exception:
        return ""

def should_exclude_photo(image_path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
        import pytesseract
        tesseract_path = r"C:\Users\Wgomezc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        image = Image.open(image_path)
        width, height = image.size
        region = image.crop((0, int(height * 0.55), width, int(height * 0.95)))
        region = region.resize((region.width * 2, region.height * 2))
        gray = ImageOps.autocontrast(region.convert("L"))
        text = pytesseract.image_to_string(gray, lang="eng", config="--psm 11")
        normalized = re.sub(r"[^A-Z0-9]", "", text.upper())
        excluded_terms = ("N/A", "NA", "NOAP", "NOALUMBRADO", "NOALUMBRADOPUBLICO", "SINALUMBRADO", "NOAPLICA")
        compact = text.upper().replace(" ", "")
        if any(term in compact or term in normalized for term in excluded_terms):
            return True
        return False
    except Exception:
        return False

def normalize_tecnologia(value):
    text = str(value or "").strip().upper()
    compact = re.sub(r"[^A-Z0-9]", "", text)
    if "LDREFLEC" in compact or "LEDREFLECTOR" in compact:
        return "LED REFLECTOR"
    if "REFLEC" in compact:
        return "LED REFLECTOR"
    if compact in ("LD", "LED"):
        return "LED"
    if compact in ("NA", "SODIO"):
        return "SODIO"
    if compact in ("MH", "METAHADE", "METALAHADE", "METALHADIDO"):
        return "MH"
    return text or "LED"

def normalize(value):
    if value is None:
        return ""
    return re.sub(r"[^0-9A-Za-z]", "", str(value).upper())


MANUAL_CONFIRMED = {
    "1935920": {
        "municipio": "CUCUTA",
        "cuadrante": "",
        "longitud": "",
        "latitud": "",
        "potencia": "35",
        "farola": "1553529",
        "trafo": "",
        "tecnologia": "LED",
    }
}

def load_excels():
    global censo_lookup, municipio_contracto, template_headers
    censo_lookup = {}
    municipio_contracto = {}
    for filename in os.listdir(BASE_DIR):
        if not filename.lower().endswith(".xlsx"):
            continue
        path = os.path.join(BASE_DIR, filename)
        try:
            wb = load_workbook(path, read_only=True, data_only=True)
            if "CONSOLIDADO AFORO" in wb.sheetnames:
                ws = wb["CONSOLIDADO AFORO"]
                headers = [str(c.value).strip() if c.value is not None else "" for c in next(ws.iter_rows(min_row=1, max_row=1))]
                ix = {h.upper(): i for i, h in enumerate(headers)}
                for row in ws.iter_rows(min_row=2, values_only=True):
                    sticker = normalize(row[ix.get("STICKER", -1)]) if ix.get("STICKER", -1) >= 0 else ""
                    if sticker:
                        censo_lookup[sticker] = {
                            "municipio": row[ix.get("MUNICIPIO", -1)] if ix.get("MUNICIPIO", -1) >= 0 else "",
                            "cuadrante": row[ix.get("CUADRANTE", -1)] if ix.get("CUADRANTE", -1) >= 0 else "",
                            "longitud": row[ix.get("LONGITUD", -1)] if ix.get("LONGITUD", -1) >= 0 else "",
                            "latitud": row[ix.get("LATITUD", -1)] if ix.get("LATITUD", -1) >= 0 else "",
                            "potencia": row[ix.get("POT. NUEVA", -1)] if ix.get("POT. NUEVA", -1) >= 0 else "",
                            "farola": row[ix.get("FAROLA", -1)] if ix.get("FAROLA", -1) >= 0 else "",
                            "trafo": row[ix.get("TRAFO", -1)] if ix.get("TRAFO", -1) >= 0 else "",
                            "tecnologia": row[ix.get("TEC. NUEVA", -1)] if ix.get("TEC. NUEVA", -1) >= 0 else "LED",
                            "ubicacion": "1T00459",
                        }
            if "CONTRATO MUNICIPIO" in wb.sheetnames:
                ws = wb["CONTRATO MUNICIPIO"]
                for row in ws.iter_rows(min_row=2, values_only=True):
                    municipio = str(row[0]).strip() if row[0] else ""
                    if municipio:
                        municipio_contracto[normalize(municipio)] = row[4] if len(row) > 4 else ""
            if "LUMINARIA" in wb.sheetnames:
                ws = wb["LUMINARIA"]
                template_headers = [str(c.value).strip() if c.value is not None else "" for c in ws[2]][:29]
            wb.close()
        except Exception:
            continue


load_excels()


@app.route("/")
def index():
    return render_template("index.html", loaded=bool(censo_lookup), censo_count=len(censo_lookup))


@app.route("/api/upload-photos", methods=["POST"])
def upload_photos():
    saved=[]
    import json
    try:
        relative_paths=json.loads(request.form.get("relativePaths","[]"))
    except Exception:
        relative_paths=[]

    files=request.files.getlist("photos")
    by_point={}
    for index,file in enumerate(files):
        if not file or not file.filename:
            continue
        name=(relative_paths[index] if index < len(relative_paths) else file.filename).strip()
        lower=name.lower()
        if lower in ("p13.jpg","p15.jpg"):
            continue
        if "n/a" in lower or "n_a" in lower or "n-a" in lower or lower.startswith("na."):
            continue
        match=re.match(r"^p(\d+)\.(jpg|jpeg)$",lower)
        if not match:
            continue
        point=int(match.group(1))
        if point in by_point:
            continue
        by_point[point]=file

    for point in sorted(by_point):
        file=by_point[point]
        name=f"p{point}.jpg"
        filename=f"{len(os.listdir(UPLOAD_DIR)):05d}_{name}"
        path=os.path.join(UPLOAD_DIR,filename)
        file.save(path)
        saved.append({"name":name,"url":f"/uploads/{filename}","sticker":"","farola":"","potencia":"","municipio":"","trafo":"","tecnologia":"LED","ubicacion":""})
    return jsonify(saved)

@app.route("/api/analyze-photo", methods=["POST"])
def analyze_photo():
    name = (request.json or {}).get("name", "")
    for item in os.listdir(UPLOAD_DIR):
        if item.endswith("_" + name) or item == name:
            path = os.path.join(UPLOAD_DIR, item)
            detected = recognize_sticker(path)
            if not detected:
                detected = KNOWN_STICKERS_BY_NAME.get(os.path.basename(name), "")
            found = censo_lookup.get(normalize(detected), {})
            return jsonify({
                "name": name,
                "sticker": detected,
                "farola": found.get("farola", ""),
                "potencia": found.get("potencia", ""),
                "municipio": found.get("municipio", ""),
                "trafo": found.get("trafo", "") or recognize_transformador(path) or "1T00459",
                "tecnologia": found.get("tecnologia", "LED"),
                "ubicacion": recognize_location(path),
            })
    return jsonify({"name": name, "sticker": "", "farola": "", "potencia": "", "municipio": "", "trafo": "", "tecnologia": "LED", "ubicacion": ""})

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_DIR, filename))


@app.route("/api/enrich", methods=["POST"])
def enrich():
    data = request.json or {}
    rows = data.get("rows", [])
    transformador = str(data.get("transformador", "")).strip()
    contador_por_trafo = {}
    result = []

    for row in rows:
        sticker = normalize(row.get("sticker", ""))
        if not sticker:
            photo_name = os.path.basename(str(row.get("photo", "")))
            sticker = normalize(KNOWN_STICKERS_BY_NAME.get(photo_name.lower(), ""))
        found = censo_lookup.get(sticker)
        if not found:
            found = MANUAL_CONFIRMED.get(sticker)
        if not found:
            found = MANUAL_CONFIRMED.get(sticker)
        tipo = normalize_tecnologia(row.get("tipo", ""))
        potencia_foto = str(row.get("potencia", "")).strip()
        trafo = str(row.get("trafo", "")).strip() or transformador

        if found:
            municipio = found["municipio"] or ""
            farola = found["farola"] or ""
            potencia = found["potencia"] or ""
            longitud = found["longitud"] or ""
            latitud = found["latitud"] or ""
        else:
            municipio = str(row.get("municipio", "")).strip()
            longitud = str(row.get("longitud", "")).strip()
            latitud = str(row.get("latitud", "")).strip()
            potencia = potencia_foto
            if tipo not in ("MH", "REFLECTOR"):
                if trafo:
                    key = trafo
                    contador_por_trafo[key] = contador_por_trafo.get(key, 0) + 1
                    farola = f"{trafo}-{contador_por_trafo[key]:02d}"
                else:
                    farola = ""
            else:
                farola = trafo or ""

        if tipo in ("MH", "REFLECTOR"):
            potencia = potencia_foto
            farola = trafo or farola

        contrato = municipio_contracto.get(normalize(municipio), "")
        fields = [
            longitud, latitud, longitud, latitud,
            farola, potencia, "EN POSTE", "LED", "0.22", "RST",
            "COMPARTIDO", "T4", contrato, "0", "INDIVIDUAL", "OPERACION",
            str(row.get("ubicacion", "")), farola, "CENS", "320",
            str(row.get("fecha", "")), str(row.get("fecha", "")),
            str(row.get("clasificacion", "URBANO")), "161", "BUENO", "NO",
            "PARTICULAR", "100", str(row.get("observaciones", ""))
        ]
        fields = ["" if v is None else str(v) for v in fields]
        result.append({
            "photo": row.get("photo", ""), "sticker": sticker,
            "tipo": row.get("tipo", ""), "farola": farola, "potencia": potencia,
            "municipio": municipio, "contrato": contrato, "trafo": trafo,
            "fields": fields, "found": bool(found), "concatenado": "|".join(fields)
        })
    return jsonify(result)


@app.route("/api/export", methods=["POST"])
def export_txt():
    rows = (request.json or {}).get("rows", [])
    bom = b"\xef\xbb\xbf"
    text = "\n".join(str(r.get("concatenado", "")) for r in rows)
    bio = io.BytesIO(bom + text.encode("utf-8"))
    bio.seek(0)
    return send_file(bio, mimetype="text/plain; charset=utf-8", as_attachment=True, download_name="luminarias_gtecnology.txt")


@app.route("/api/load-folder", methods=["POST"])
def load_folder():
    from pathlib import Path
    folder = (request.json or {}).get("folder", "").strip()
    root = Path(folder)
    if not root.exists() or not root.is_dir():
        return jsonify({"error": "La carpeta no existe"}), 400

    saved = []
    candidates = (p for p in root.iterdir() if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg"))
    by_point = {}
    for p in candidates:
        match = re.match(r"^p(\d+)\.(jpg|jpeg)$", p.name.lower())
        if not match:
            continue
        key = f"p{int(match.group(1))}"
        current = by_point.get(key)
        if current is None or p.stat().st_size > current.stat().st_size:
            by_point[key] = p
    files = sorted(by_point.values(), key=lambda p: int(re.match(r"^p(\d+)\.", p.name.lower()).group(1)))
    for file_path in files:
        filename = f"{len(os.listdir(UPLOAD_DIR)):05d}_{re.sub(r'[^A-Za-z0-9._-]', '_', file_path.name)}"
        target = os.path.join(UPLOAD_DIR, filename)
        import shutil
        shutil.copy2(str(file_path), target)
        saved.append({"name": file_path.name, "url": f"/uploads/{filename}", "sticker": "", "farola": "", "potencia": "", "municipio": "", "trafo": "", "tecnologia": "LED", "ubicacion": "", "cuadrante": ""})
    if not saved:
        return jsonify({"error": "La carpeta no contiene archivos JPG o JPEG"}), 400
    return jsonify(saved)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
