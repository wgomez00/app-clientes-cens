from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = p.read_text(encoding="utf-8")
old = "render();\n</script>"
new = """render();
const hoy=new Date();
const fechaHoy=`${hoy.getFullYear()}-${String(hoy.getMonth()+1).padStart(2,'0')}-${String(hoy.getDate()).padStart(2,'0')}`;
document.getElementById('fecha').value=fechaHoy;
document.getElementById('observaciones').value=`AP-AFORO-${fechaHoy}`;
const folderOriginal=document.getElementById('folderPath').value;
const partes=folderOriginal.split(/\\\\|\\//);
const posibleSeccion=partes.find(x=>/NIÑA|NINA|SECTOR|BARRIO/i.test(x));
if(posibleSeccion) document.getElementById('ubicacion').value=posibleSeccion;

async function loadResultPopulatesFields(data){
  const primero=data.find(x=>x.sticker && x.municipio);
  if(!primero)return;
  if(primero.municipio)document.getElementById('municipio').value=primero.municipio;
  if(primero.trafo)document.getElementById('transformador').value=primero.trafo;
  document.getElementById('clasificacion').value=/CUCUTA|CUCÚTA|NORTE/i.test(primero.municipio||'')?'URBANO':'URBANO';
}
</script>"""
if old in s:
    s = s.replace(old, new)
s = s.replace('  photos.push(...data.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:\'base\'})));\n  render();', '  photos.push(...data.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:\'base\'})));\n  loadResultPopulatesFields(data);\n  render();')
s = s.replace('  photos.push(...nuevas.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:\'base\'})));\n  render();', '  photos.push(...nuevas.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:\'base\'})));\n  loadResultPopulatesFields(nuevas);\n  render();')
p.write_text(s, encoding="utf-8")
