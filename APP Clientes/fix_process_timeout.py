from pathlib import Path

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = app.read_text(encoding="utf-8")
old = '''            if not sticker:
                for uploaded in os.listdir(UPLOAD_DIR):
                    if uploaded == photo_name or uploaded.endswith("_" + photo_name):
                        sticker = normalize(recognize_sticker(os.path.join(UPLOAD_DIR, uploaded)))
                        break
'''
s = s.replace(old, '')
app.write_text(s, encoding="utf-8")

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = html.read_text(encoding="utf-8")
start = t.find("document.getElementById('process').onclick=async()=>{")
end = t.find("function renderResults(){", start)
if start >= 0 and end >= 0:
    block = '''document.getElementById('process').onclick=async()=>{
  if(!photos.length){ alert('Carga al menos una carpeta o algunas fotos antes de procesar'); return; }
  const boton=document.getElementById('process');
  boton.disabled=true;
  boton.textContent='Procesando...';
  const controlador=new AbortController();
  const temporizador=setTimeout(()=>controlador.abort(),15000);
  try{
    const respuesta=await fetch('/api/enrich',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({transformador:document.getElementById('transformador').value,rows:collect()}),signal:controlador.signal});
    clearTimeout(temporizador);
    if(!respuesta.ok)throw new Error(`Error del servidor ${respuesta.status}`);
    resultRows=await respuesta.json();
    renderResults();
    document.getElementById('results').scrollIntoView({behavior:'smooth',block:'start'});
  }catch(error){
    document.getElementById('results').innerHTML=`<div class="empty">No se pudo procesar: ${esc(error.name==='AbortError'?'La solicitud excedió 15 segundos':error.message)}</div>`;
  }finally{
    clearTimeout(temporizador);
    boton.disabled=false;
    boton.textContent='Procesar luminarias';
  }
};
'''
    t=t[:start]+block+t[end:]
html.write_text(t, encoding="utf-8")
