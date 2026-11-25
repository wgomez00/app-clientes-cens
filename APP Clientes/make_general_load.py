from pathlib import Path

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = html.read_text(encoding="utf-8")

start = s.find('      <label>Ruta local de la carpeta</label>')
if start >= 0:
    end = s.find('    </aside>', start)
    s = s[:start] + '    </aside>' + s[end+12:] if end >= 0 else s

s = s.replace('Arrastra aquí la carpeta con las fotos<br><small>o selecciona una carpeta completa</small>', 'Arrastra aquí cualquier carpeta de fotos<br><small>o haz clic y selecciona una carpeta completa</small>')

old_load = '''document.getElementById('loadFolder').onclick=async()=>{
  const folder=document.getElementById('folderPath').value.trim();
  if(!folder)return alert('Ingresa la ruta de la carpeta');
  const r=await fetch('/api/load-folder',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({folder})});
  const data=await r.json();
  if(!r.ok)return alert(data.error||'No se pudo cargar la carpeta');
  photos.push(...data.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'})));
  render();
  analyzePhotos(data);
};'''
if old_load in s:
    s = s.replace(old_load, '')

html.write_text(s, encoding="utf-8")

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
t = app.read_text(encoding="utf-8")
t = t.replace('tesseract_path = r"C:\\Users\\Wgomezc\\AppData\\Local\\Programs\\Tesseract-OCR\tesseract.exe"', 'tesseract_path = r"C:\\Users\\Wgomezc\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"')
app.write_text(t, encoding="utf-8")
