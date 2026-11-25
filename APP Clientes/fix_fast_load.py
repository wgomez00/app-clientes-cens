from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = p.read_text(encoding="utf-8")

# Elimina OCR bloqueante del cargue por navegador.
old = '''            detected = recognize_sticker(path)
            found = censo_lookup.get(normalize(detected), {})
            saved.append({
                "name": relative.replace("\\\\", "/"),
                "url": f"/uploads/{filename}",
                "sticker": detected,
                "farola": found.get("farola", ""),
                "potencia": found.get("potencia", ""),
                "municipio": found.get("municipio", ""),
                "trafo": found.get("trafo", ""),
                "tecnologia": found.get("tecnologia", "LED"),
            })'''
new = '''            saved.append({
                "name": relative.replace("\\\\", "/"),
                "url": f"/uploads/{filename}",
                "sticker": "",
                "farola": "",
                "potencia": "",
                "municipio": "",
                "trafo": "",
                "tecnologia": "LED",
            })'''
s = s.replace(old, new)

# Elimina OCR bloqueante del cargue directo y conserva deduplicación por punto.
old2 = '''        detected = recognize_sticker(str(file_path))
        found = censo_lookup.get(normalize(detected), {})
        saved.append({
            "name": file_path.name,
            "url": f"/uploads/{filename}",
            "sticker": detected,
            "farola": found.get("farola", ""),
            "potencia": found.get("potencia", ""),
            "municipio": found.get("municipio", ""),
            "trafo": found.get("trafo", ""),
            "tecnologia": found.get("tecnologia", "LED"),
            "ubicacion": "",
        })'''
new2 = '''        saved.append({
            "name": file_path.name,
            "url": f"/uploads/{filename}",
            "sticker": "",
            "farola": "",
            "potencia": "",
            "municipio": "",
            "trafo": "",
            "tecnologia": "LED",
            "ubicacion": "",
        })'''
s = s.replace(old2, new2)

# Endpoint ligero de análisis individual.
marker = '@app.route("/uploads/<path:filename>")\n'
endpoint = '''@app.route("/api/analyze-photo", methods=["POST"])
def analyze_photo():
    name = (request.json or {}).get("name", "")
    for item in os.listdir(UPLOAD_DIR):
        if item.endswith("_" + name) or item == name:
            path = os.path.join(UPLOAD_DIR, item)
            detected = recognize_sticker(path)
            found = censo_lookup.get(normalize(detected), {})
            return jsonify({
                "name": name,
                "sticker": detected,
                "farola": found.get("farola", ""),
                "potencia": found.get("potencia", ""),
                "municipio": found.get("municipio", ""),
                "trafo": found.get("trafo", ""),
                "tecnologia": found.get("tecnologia", "LED"),
                "ubicacion": "",
            })
    return jsonify({"name": name, "sticker": "", "farola": "", "potencia": "", "municipio": "", "trafo": "", "tecnologia": "LED", "ubicacion": ""})

'''
if '@app.route("/api/analyze-photo"' not in s:
    s = s.replace(marker, endpoint + marker)

p.write_text(s, encoding="utf-8")

h = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = h.read_text(encoding="utf-8")
old_render = '''  const nuevas=await r.json();
  photos.push(...nuevas.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'})));
  loadResultPopulatesFields(nuevas);
  render();'''
new_render = '''  const nuevas=await r.json();
  photos.push(...nuevas.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'})));
  render();
  analyzePhotos(nuevas);'''
t = t.replace(old_render, new_render)
old_direct = '''  photos.push(...data.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'})));
  loadResultPopulatesFields(data);
  render();'''
new_direct = '''  photos.push(...data.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'})));
  render();
  analyzePhotos(data);'''
t = t.replace(old_direct, new_direct)

marker2 = "async function upload(files){"
block = '''async function analyzePhotos(items){
  for(let i=0;i<items.length;i++){
    const item=items[i];
    try{
      const r=await fetch('/api/analyze-photo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:item.name})});
      const info=await r.json();
      const index=photos.findIndex(p=>p.name===item.name);
      if(index>=0){
        photos[index]={...photos[index],...info};
        const card=document.querySelectorAll('.photo')[index];
        if(card){
          if(info.sticker)card.querySelector('.sticker').value=info.sticker;
          if(info.potencia)card.querySelector('.potencia').value=info.potencia;
          if(info.farola)card.querySelector('.farola').value=info.farola;
          if(info.tecnologia){
            [...card.querySelector('.tipo').options].forEach(o=>o.selected=o.text===info.tecnologia.toUpperCase());
          }
        }
      }
    }catch(e){}
  }
  loadResultPopulatesFields(photos);
}

async function upload(files){'''
if marker2 in t:
    t = t.replace(marker2, block)

h.write_text(t, encoding="utf-8")
