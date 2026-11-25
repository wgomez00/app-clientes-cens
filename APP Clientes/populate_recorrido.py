from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = p.read_text(encoding="utf-8")

old = '''  const hoy=new Date();
const fechaHoy=`${hoy.getFullYear()}-${String(hoy.getMonth()+1).padStart(2,'0')}-${String(hoy.getDate()).padStart(2,'0')}`;
document.getElementById('fecha').value=fechaHoy;
document.getElementById('observaciones').value=`AP-AFORO-${fechaHoy}`;
async function loadResultPopulatesFields(data){'''
new = '''  function actualizarFechaRecorrido(){
  const hoy=new Date();
  const fechaHoy=`${hoy.getFullYear()}-${String(hoy.getMonth()+1).padStart(2,'0')}-${String(hoy.getDate()).padStart(2,'0')}`;
  document.getElementById('fecha').value=fechaHoy;
  document.getElementById('observaciones').value=`AP-AFORO-${fechaHoy}`;
}
actualizarFechaRecorrido();

async function loadResultPopulatesFields(data){'''
if old in s:
    s = s.replace(old, new)

old_load = '''  const primero=data.find(x=>x.sticker && x.municipio);
  if(!primero)return;
  if(primero.municipio)document.getElementById('municipio').value=primero.municipio;
  if(primero.trafo)document.getElementById('transformador').value=primero.trafo;
  if(primero.ubicacion)document.getElementById('ubicacion').value=primero.ubicacion;
  document.getElementById('clasificacion').value='URBANO';
}'''
new_load = '''  actualizarFechaRecorrido();
  const primero=data.find(x=>x.sticker && x.municipio);
  if(!primero)return;
  if(primero.municipio)document.getElementById('municipio').value=primero.municipio;
  if(primero.trafo)document.getElementById('transformador').value=primero.trafo;
  if(primero.ubicacion)document.getElementById('ubicacion').value=primero.ubicacion;
  document.getElementById('clasificacion').value='URBANO';
}'''
if old_load in s:
    s = s.replace(old_load, new_load)

# Actualiza fecha y observaciones al iniciar el cargador y al cargar más fotos.
s = s.replace("  photos=[];\n  photos.push", "  actualizarFechaRecorrido();\n  photos=[];\n  photos.push")

p.write_text(s, encoding="utf-8")
