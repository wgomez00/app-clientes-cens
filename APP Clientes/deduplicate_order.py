from pathlib import Path

html=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=html.read_text(encoding="utf-8")
start=s.find("async function subirArchivos(files){")
end=s.find("drop.onclick=()=>input.click();",start)
if start>=0 and end>=0:
    block='''async function subirArchivos(files){
  const vistos=new Set();
  const seleccionados=[...files].filter(f=>{
    const nombre=f.name.trim().toLowerCase();
    if(nombre==='p13.jpg'||nombre==='p15.jpg')return false;
    if(nombre.includes('n/a')||nombre.includes('n_a')||nombre.includes('n-a')||/^na\./.test(nombre))return false;
    if(/\\.(jpg|jpeg)$/i.test(nombre)===false)return false;
    const punto=nombre.match(/^p(\\d+)\\.(jpg|jpeg)$/i);
    if(!punto)return false;
    const clave=`p${parseInt(punto[1],10)}`;
    if(vistos.has(clave))return false;
    vistos.add(clave);
    return true;
  }).sort((a,b)=>{
    const na=parseInt(a.name.match(/^p(\\d+)/i)?.[1]||'999999',10);
    const nb=parseInt(b.name.match(/^p(\\d+)/i)?.[1]||'999999',10);
    return na-nb;
  });

  if(!seleccionados.length){alert('No hay fotos JPG válidas');return;}
  const form=new FormData();
  seleccionados.forEach(f=>form.append('photos',f));
  form.append('relativePaths',JSON.stringify(seleccionados.map(f=>f.name)));
  const r=await fetch('/api/upload-photos',{method:'POST',body:form});
  if(!r.ok){alert('Error al cargar las fotos');return;}
  const data=await r.json();
  photos=data.sort((a,b)=>{
    const na=parseInt(a.name.match(/^p(\\d+)/i)?.[1]||'999999',10);
    const nb=parseInt(b.name.match(/^p(\\d+)/i)?.[1]||'999999',10);
    return na-nb;
  });
  render();
}
'''
    s=s[:start]+block+s[end:]
html.write_text(s,encoding="utf-8")

app=Path(r"C:\MDEsmart\APP Clientes\app.py")
t=app.read_text(encoding="utf-8")
old='''            relative = relative_paths[index] if index < len(relative_paths) else file.filename
'''
# No need to change backend; frontend controls the deduplication and order.
app.write_text(t,encoding="utf-8")
