from pathlib import Path

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = app.read_text(encoding="utf-8")
s = s.replace('                            "trafo": row[ix.get("TRAFO", -1)] if ix.get("TRAFO", -1) >= 0 else "",\n                        }', '                            "trafo": row[ix.get("TRAFO", -1)] if ix.get("TRAFO", -1) >= 0 else "",\n                            "tecnologia": row[ix.get("TEC. NUEVA", -1)] if ix.get("TEC. NUEVA", -1) >= 0 else "LED",\n                        }')
old = '''            path = os.path.join(UPLOAD_DIR, filename)
            file.save(path)
            saved.append({"name": relative.replace("\\", "/"), "url": f"/uploads/{filename}"})
'''
new = '''            path = os.path.join(UPLOAD_DIR, filename)
            file.save(path)
            detected = recognize_sticker(path)
            found = censo_lookup.get(normalize(detected), {})
            saved.append({
                "name": relative.replace("\\", "/"),
                "url": f"/uploads/{filename}",
                "sticker": detected,
                "farola": found.get("farola", ""),
                "potencia": found.get("potencia", ""),
                "municipio": found.get("municipio", ""),
                "trafo": found.get("trafo", ""),
                "tecnologia": found.get("tecnologia", "LED"),
                "cuadrante": found.get("cuadrante", ""),
            })
'''
if old in s:
    s = s.replace(old, new)
old_load = '''        detected = recognize_sticker(str(file_path))
        saved.append({"name": file_path.name, "url": f"/uploads/{filename}", "sticker": detected})
'''
new_load = '''        detected = recognize_sticker(str(file_path))
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
            "cuadrante": found.get("cuadrante", ""),
        })
'''
if old_load in s:
    s = s.replace(old_load, new_load)
app.write_text(s, encoding="utf-8")

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = html.read_text(encoding="utf-8")
start = 'function photoCard(p,i){return '
line_end = '\nfunction render'
start_idx = t.find(start)
end_idx = t.find(line_end, start_idx)
if start_idx >= 0 and end_idx >= 0:
    new_card = '''function photoCard(p,i){return `<div class="photo"><img src="${esc(p.url)}" alt="Foto"><div class="photo-body"><strong>${esc(p.name)}</strong><div class="mini-grid"><label>Código sticker<input class="sticker" data-i="${i}" value="${esc(p.sticker||'')}" placeholder="Ej. 1900679"></label><label>Potencia<input class="potencia" data-i="${i}" value="${esc(p.potencia||'')}" placeholder="Ej. 35"></label><label>Tecnología<select class="tipo" data-i="${i}"><option${p.tecnologia==='LED'?' selected':''}>LED</option><option${p.tecnologia==='MH'?' selected':''}>MH</option><option${p.tecnologia==='SODIO'?' selected':''}>SODIO</option></select></label><label>Farola<input class="farola" data-i="${i}" value="${esc(p.farola||'')}" readonly></label></div></div></div>`}
'''
    t = t[:start_idx] + new_card + t[end_idx+1:] 
old_upload = '''  const selected=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name)||/^image\\/jpeg$/i.test(f.type));'''
new_upload = '''  const selected=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name) && !/\\.{2}\.jpg$/i.test(f.name) && !f.name.includes('_thumb')).filter((f,i,a)=>{
    const base=f.name.replace(/\\.(jpg|jpeg)$/i,'').replace(/[_-]?\d+$/,'');
    return a.findIndex(x=>x.name.replace(/\\.(jpg|jpeg)$/i,'').replace(/[_-]?\d+$/,'')===base)===i;
  });'''
if old_upload in t:
    t = t.replace(old_upload,new_upload)
html.write_text(t, encoding="utf-8")
