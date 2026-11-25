from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
marker='render();\nconst hoy=new Date();'
block='''// Cargador definitivo
input.removeAttribute('hidden');
input.onchange=null;
input.addEventListener('change',async function(e){
  const files=[...(e.target.files||[])].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name));
  if(!files.length)return;
  const form=new FormData();
  files.forEach(f=>form.append('photos',f));
  form.append('relativePaths',JSON.stringify(files.map(f=>f.name)));
  const r=await fetch('/api/upload-photos',{method:'POST',body:form});
  if(!r.ok){alert('Error al cargar fotos');return;}
  const nuevas=await r.json();
  photos=nuevas;
  render();
});
drop.onclick=()=>input.click();

'''
# Replace all old onchange handlers with one defensive listener.
if marker in s:
    s=s.replace(marker,block+marker)
p.write_text(s,encoding="utf-8")
