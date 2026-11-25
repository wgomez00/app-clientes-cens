from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
start=s.find("async function upload(files){")
end=s.find("function collect(){",start)
if start>=0 and end>=0:
    block='''async function upload(files){
  const selected=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name));
  if(!selected.length){ alert('La carpeta no contiene archivos JPG'); return; }
  const form=new FormData();
  selected.forEach(f=>form.append('photos',f));
  form.append('relativePaths',JSON.stringify(selected.map(f=>f.name)));
  try{
    const r=await fetch('/api/upload-photos',{method:'POST',body:form});
    if(!r.ok)throw new Error('Error al subir '+r.status);
    const nuevas=await r.json();
    photos=[];
    photos.push(...nuevas);
    render();
  }catch(error){
    alert(error.message);
  }
}
'''
    s=s[:start]+block+s[end:]
p.write_text(s,encoding="utf-8")
