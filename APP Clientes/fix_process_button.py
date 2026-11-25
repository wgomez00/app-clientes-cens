from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
old='document.getElementById(\'process\').onclick=async()=>{if(!photos.length)return alert(\'Carga al menos una foto\');const r=await fetch(\'/api/enrich\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify({transformador:document.getElementById(\'transformador\').value,rows:collect()})});resultRows=await r.json();renderResults()};'
new='''document.getElementById('process').onclick=async()=>{
  if(!photos.length){ alert('Carga al menos una carpeta o algunas fotos antes de procesar'); return; }
  const boton=document.getElementById('process');
  boton.disabled=true;
  boton.textContent='Procesando...';
  try{
    const respuesta=await fetch('/api/enrich',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({transformador:document.getElementById('transformador').value,rows:collect()})});
    if(!respuesta.ok)throw new Error(`Error del servidor ${respuesta.status}`);
    resultRows=await respuesta.json();
    renderResults();
    document.getElementById('results').scrollIntoView({behavior:'smooth',block:'start'});
  }catch(error){
    document.getElementById('results').innerHTML=`<div class="empty">No se pudo procesar: ${esc(error.message)}</div>`;
  }finally{
    boton.disabled=false;
    boton.textContent='Procesar luminarias';
  }
};'''
if old not in s:
    raise SystemExit('Manejador antiguo no encontrado')
p.write_text(s.replace(old,new),encoding="utf-8")
