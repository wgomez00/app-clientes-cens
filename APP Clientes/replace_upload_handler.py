from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
old='input.onchange=e=>{ if(e.target.files?.length) upload(e.target.files); };'
new='''input.onchange=async function(e){
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
if old in s:
    s=s.replace(old,new)
else:
    marker="drop.onclick=()=>input.click();"
    s=s.replace(marker,marker+'\n'+new)
p.write_text(s,encoding="utf-8")
