from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
old='''input.onchange=async function(e){
  if(!e.target.files?.length)return;
  const form=new FormData();
  [...e.target.files].forEach(file=>form.append('photos',file));
  form.append('relativePaths',JSON.stringify([...e.target.files].map(file=>file.name)));
  try{
    const respuesta=await fetch('/api/upload-photos',{method:'POST',body:form});
    if(!respuesta.ok)throw new Error('Error al subir '+respuesta.status);
    const nuevas=await respuesta.json();
    photos=nuevas;
    render();
  }catch(error){ alert(error.message); }
};'''
new='''input.onchange=function(e){
  if(!e.target.files || !e.target.files.length)return;
  const form=new FormData();
  for(const file of e.target.files) form.append('photos',file);
  form.append('relativePaths',JSON.stringify([...e.target.files].map(file=>file.name)));
  fetch('/api/upload-photos',{method:'POST',body:form}).then(r=>{
    if(!r.ok)throw new Error('Error al subir '+r.status);
    return r.json();
  }).then(nuevas=>{photos=nuevas;render();}).catch(error=>alert(error.message));
};'''
s=s.replace(old,new)
p.write_text(s,encoding="utf-8")
