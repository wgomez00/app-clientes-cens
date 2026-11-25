from pathlib import Path

app=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=app.read_text(encoding="utf-8")

# Add OCR for circuit and location after recognized sticker.
marker='def recognize_location(image_path):\n'
if 'def recognize_transformador' not in s:
    extra='''def recognize_transformador(image_path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
        import pytesseract
        tesseract_path = r"C:\\Users\\Wgomezc\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
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

'''
    s=s.replace(marker,extra+marker)

app.write_text(s,encoding="utf-8")

html=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t=html.read_text(encoding="utf-8")
old='''async function subirArchivos(files){
'''
new='''async function subirArchivos(files){
'''
# The existing loader will remain; add response processing in the success branch.
old_data='''  const data=await r.json();
  photos=data.sort((a,b)=>{
'''
new_data='''  const data=await r.json();
  photos=data.sort((a,b)=>{
'''
# Processed data already arrives; populate generic fields after all cards render.
old_after='''  render();
}
'''
new_after='''  render();
  actualizarDatosRecorrido(photos);
}
'''
# Insert only first matching occurrence in subirArchivos block.
idx=t.find("  const data=await r.json();",t.find("async function subirArchivos"))
if idx>=0:
    old_sub='''  const data=await r.json();
  photos=data.sort((a,b)=>{
'''
    new_sub='''  const data=await r.json();
  photos=data.sort((a,b)=>{
'''
    if old_sub in t:
        t=t.replace(old_sub,new_sub,1)

# Add helper before collect, not before final script date setup.
marker='function collect(){'
helper='''async function actualizarDatosRecorrido(fotos){
  const hoy=new Date();
  const fechaHoy=`${hoy.getFullYear()}-${String(hoy.getMonth()+1).padStart(2,'0')}-${String(hoy.getDate()).padStart(2,'0')}`;
  document.getElementById('fecha').value=fechaHoy;
  document.getElementById('observaciones').value=`AP-AFORO-${fechaHoy}`;

  for(const foto of fotos||[]){
    const input=await fetch('/api/analyze-photo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:foto.name})});
    if(!input.ok)continue;
    const info=await input.json();
    if(info.excluded)continue;
    if(info.municipio){
      document.getElementById('municipio').value=info.municipio;
      const municipio=info.municipio.toUpperCase();
      const rurales=['ABREGO','ARBOLEDAS','BOCALEMA','BUCARASICA','CACOTA','CONVENCION','CUCUTILLA','EL TARRA','LABATECA','LOS PATIOS','PAMPLONA','PAMPLONITA','RAGONVALIA','SALAZAR','SAN CALIXTO','SAN CAYETANO','SANTIAGO','SARDINATA','TEORAMA','TIBU','VILLA CARO','VILLA DEL ROSARIO'];
      document.getElementById('clasificacion').value=rurales.some(r=>municipio.includes(r))?'RURAL':'URBANO';
    }
    if(info.trafo)document.getElementById('transformador').value=info.trafo;
    if(info.ubicacion)document.getElementById('ubicacion').value=info.ubicacion;
  }
}

'''
if marker in t:
    t=t.replace(marker,helper+marker)
html.write_text(t,encoding="utf-8")
