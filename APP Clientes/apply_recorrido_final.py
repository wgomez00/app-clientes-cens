from pathlib import Path

html_path = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
html = html_path.read_text(encoding="utf-8")
html = html.replace('<label>Transformador principal</label><input id="transformador" placeholder="Ej. 1T01019">', '<label>Transformador principal</label><input id="transformador" value="1T00459" placeholder="Ej. 1T00459">')
html = html.replace('<label>Municipio predeterminado</label><input id="municipio" placeholder="Ej. CÚCUTA">', '<label>Municipio predeterminado</label><input id="municipio" value="CUCUTA" placeholder="Ej. CÚCUTA">')
html = html.replace('<label>Ubicación</label><input id="ubicacion" placeholder="Barrio o sector">', '<label>Ubicación / Circuito</label><input id="ubicacion" value="1T00459" placeholder="Ej. 1T00459">')
html = html.replace('<div class="drop" id="drop">Arrastra aquí­', '<div class="drop" id="drop">Arrastra aquí')

old = '''  const selected=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name) && !/\\.{2}\\.jpg$/i.test(f.name) && !f.name.includes('_thumb')).filter((f,i,a)=>{
    const base=f.name.replace(/\\.(jpg|jpeg)$/i,'').replace(/[_-]?\\d+$/,'');
    return a.findIndex(x=>x.name.replace(/\\.(jpg|jpeg)$/i,'').replace(/[_-]?\\d+$/,'')===base)===i;
  });'''
new = '''  const normal=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name));
  const selected=[];
  const vistos=new Set();
  normal.sort((a,b)=>String(a.webkitRelativePath||a.name).localeCompare(String(b.webkitRelativePath||b.name),undefined,{numeric:true,sensitivity:'base'}));
  for(const f of normal){
    const nombre=f.name.toLowerCase();
    const punto=nombre.match(/^p(\\d+)\\.(jpg|jpeg)$/);
    const clave=punto ? `p${punto[1]}` : nombre.replace(/\\.(jpg|jpeg)$/,'');
    if(vistos.has(clave)) continue;
    vistos.add(clave);
    selected.push(f);
  }'''
if old in html:
    html = html.replace(old, new)

html = html.replace('const posibleSeccion=partes.find(x=>/NIÑA|NINA|SECTOR|BARRIO/i.test(x));\nif(posibleSeccion) document.getElementById(\'ubicacion\').value=posibleSeccion;', "document.getElementById('transformador').value='1T00459';\ndocument.getElementById('municipio').value='CUCUTA';\ndocument.getElementById('ubicacion').value='1T00459';")
html = html.replace("document.getElementById('clasificacion').value=/CUCUTA|CUCÚTA|NORTE/i.test(primero.municipio||'')?'URBANO':'URBANO';", "document.getElementById('clasificacion').value='URBANO';")
html_path.write_text(html, encoding="utf-8")

app_path = Path(r"C:\MDEsmart\APP Clientes\app.py")
app = app_path.read_text(encoding="utf-8")
old_load = '''    files = sorted(
        (p for p in root.iterdir() if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg") and ".." not in p.name),
        key=lambda p: p.name.lower()
    )'''
new_load = '''    candidates = (p for p in root.iterdir() if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg"))
    by_point = {}
    for p in candidates:
        match = re.match(r"^p(\\d+)\\.(jpg|jpeg)$", p.name.lower())
        if not match:
            continue
        key = f"p{int(match.group(1))}"
        current = by_point.get(key)
        if current is None or p.stat().st_size > current.stat().st_size:
            by_point[key] = p
    files = sorted(by_point.values(), key=lambda p: int(re.match(r"^p(\\d+)\\.", p.name.lower()).group(1)))'''
if old_load in app:
    app = app.replace(old_load, new_load)
app_path.write_text(app, encoding="utf-8")
