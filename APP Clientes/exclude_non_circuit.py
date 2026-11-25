from pathlib import Path

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = app.read_text(encoding="utf-8")
marker = 'def normalize(value):\n'
func = '''def should_exclude_photo(image_path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
        import pytesseract
        tesseract_path = r"C:\\Users\\Wgomezc\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
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

'''
if 'def should_exclude_photo' not in s:
    s = s.replace(marker, func + marker)

# Skip excluded photos in browser upload endpoint.
old = '''            file.save(path)
            saved.append({"name": relative.replace("\\\\", "/"), "url": f"/uploads/{filename}", "sticker": "", "farola": "", "potencia": "", "municipio": "", "trafo": "", "tecnologia": "LED", "ubicacion": ""})
'''
new = '''            file.save(path)
            if should_exclude_photo(path):
                os.remove(path)
                continue
            saved.append({"name": relative.replace("\\\\", "/"), "url": f"/uploads/{filename}", "sticker": "", "farola": "", "potencia": "", "municipio": "", "trafo": "", "tecnologia": "LED", "ubicacion": ""})
'''
s = s.replace(old, new)

# Return excluded status from individual analysis.
old_analyze = '''            found = censo_lookup.get(normalize(detected), {})
            return jsonify({
'''
new_analyze = '''            found = censo_lookup.get(normalize(detected), {})
            if should_exclude_photo(path):
                return jsonify({"name": name, "excluded": True, "sticker": "", "farola": "", "potencia": "", "municipio": "", "trafo": "", "tecnologia": "", "ubicacion": ""})
            return jsonify({
'''
s = s.replace(old_analyze, new_analyze)
app.write_text(s, encoding="utf-8")

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = html.read_text(encoding="utf-8")
old_js = '''      const info=await r.json();
      const index=photos.findIndex(p=>p.name===item.name);
'''
new_js = '''      const info=await r.json();
      if(info.excluded){
        photos=photos.filter(p=>p.name!==item.name);
        render();
        continue;
      }
      const index=photos.findIndex(p=>p.name===item.name);
'''
if old_js in t:
    t = t.replace(old_js, new_js)
html.write_text(t, encoding="utf-8")
