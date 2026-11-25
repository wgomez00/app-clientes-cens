from pathlib import Path

html_path = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
html = html_path.read_text(encoding="utf-8")
html = html.replace('<label>Transformador principal</label><input id="transformador" value="1T00459" placeholder="Ej. 1T00459">', '<label>Transformador principal</label><input id="transformador" value="" placeholder="Ej. 1T00459">')
html = html.replace('<label>Municipio predeterminado</label><input id="municipio" value="CUCUTA" placeholder="Ej. CÚCUTA">', '<label>Municipio predeterminado</label><input id="municipio" value="" placeholder="Ej. CÚCUTA">')
html = html.replace('<label>Ubicación</label><input id="ubicacion" value="1T00459" placeholder="Ubicación del recorrido">', '<label>Ubicación</label><input id="ubicacion" value="" placeholder="Se completa al reconocer una dirección en la foto">')

old_init = "document.getElementById('transformador').value='1T00459';\ndocument.getElementById('municipio').value='CUCUTA';\ndocument.getElementById('ubicacion').value='1T00459';"
html = html.replace(old_init, "")

old_populate = """  if(primero.municipio)document.getElementById('municipio').value=primero.municipio;
  if(primero.trafo)document.getElementById('transformador').value=primero.trafo;
  if(primero.ubicacion)document.getElementById('ubicacion').value=primero.ubicacion;
  if(!document.getElementById('ubicacion').value)document.getElementById('ubicacion').value='1T00459';
  document.getElementById('clasificacion').value='URBANO';"""
new_populate = """  if(primero.municipio)document.getElementById('municipio').value=primero.municipio;
  if(primero.trafo)document.getElementById('transformador').value=primero.trafo;
  if(primero.ubicacion)document.getElementById('ubicacion').value=primero.ubicacion;
  if(!document.getElementById('transformador').value){
    const ruta=document.getElementById('folderPath').value;
    const circuito=(ruta.match(/(^|\\\\|\\/)([0-9]+T[0-9]+)/i)||[])[2];
    if(circuito)document.getElementById('transformador').value=circuito;
  }
  document.getElementById('clasificacion').value='URBANO';"""
html = html.replace(old_populate, new_populate)
html_path.write_text(html, encoding="utf-8")

app_path = Path(r"C:\MDEsmart\APP Clientes\app.py")
app = app_path.read_text(encoding="utf-8")
needle = 'def normalize(value):\n'
ocr_location = '''def recognize_location(image_path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
        import pytesseract
        tesseract_path = r"C:\\Users\Wgomezc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
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
            line = re.sub(r"\\s+", " ", line).strip(" ,.-")
            if address_markers.match(line) and len(line) >= 5:
                return line[:120]
        return ""
    except Exception:
        return ""

'''
if ocr_location not in app:
    app = app.replace(needle, ocr_location + needle, 1)

# Add location and circuit fields in direct load_folder response.
app = app.replace('            "tecnologia": found.get("tecnologia", "LED"),\n            "cuadrante": found.get("cuadrante", ""),', '            "tecnologia": found.get("tecnologia", "LED"),\n            "ubicacion": recognize_location(str(file_path)),\n            "cuadrante": found.get("cuadrante", ""),')
app = app.replace('                "tecnologia": found.get("tecnologia", "LED"),\n            })', '                "tecnologia": found.get("tecnologia", "LED"),\n                "ubicacion": recognize_location(path),\n            })')
app_path.write_text(app, encoding="utf-8")
