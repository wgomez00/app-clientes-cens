from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
start=s.find("async function loadResultPopulatesFields")
end=s.find("</script>",start)
new='''async function loadResultPopulatesFields(data){
  actualizarFechaRecorrido();
  const primero=(data||[]).find(x=>x && x.sticker && x.municipio);
  if(!primero)return;
  if(primero.municipio)document.getElementById('municipio').value=primero.municipio;
  if(primero.trafo)document.getElementById('transformador').value=primero.trafo;
  if(primero.ubicacion)document.getElementById('ubicacion').value=primero.ubicacion;
  document.getElementById('clasificacion').value='URBANO';
}
function actualizarFechaRecorrido(){
  const hoy=new Date();
  const fechaHoy=`${hoy.getFullYear()}-${String(hoy.getMonth()+1).padStart(2,'0')}-${String(hoy.getDate()).padStart(2,'0')}`;
  document.getElementById('fecha').value=fechaHoy;
  document.getElementById('observaciones').value=`AP-AFORO-${fechaHoy}`;
}
actualizarFechaRecorrido();
'''
if start>=0 and end>=0:
    s=s[:start]+new+s[end:]
p.write_text(s,encoding="utf-8")
