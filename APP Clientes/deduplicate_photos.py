from pathlib import Path

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = html.read_text(encoding="utf-8")
start = s.find("async function upload(files){")
end = s.find("function collect()", start)
if start >= 0 and end >= 0:
    block = '''async function upload(files){
  const normales=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name));
  const selected=[];
  const vistos=new Set();

  normales.sort((a,b)=>String(a.webkitRelativePath||a.name).localeCompare(String(b.webkitRelativePath||b.name),undefined,{numeric:true,sensitivity:'base'}));

  for(const f of normales){
    const nombre=f.name.trim().toLowerCase();
    if(nombre.includes('thumb') || nombre.includes('mini') || nombre.includes('preview')) continue;

    let clave=nombre.replace(/\\s+/g,'')
      .replace(/\\.(jpg|jpeg)$/,'')
      .replace(/\\.+$/,'')
      .replace(/[_-]?\\d{2,3}$/,'');

    const punto=nombre.match(/^p(\\d+)\\.*\\.(jpg|jpeg)$/);
    if(punto) clave=`p${parseInt(punto[1],10)}`;

    if(vistos.has(clave)) continue;
    vistos.add(clave);
    selected.push(f);
  }

  if(!selected.length)return alert('La carpeta no contiene imágenes compatibles');
  selected.sort((a,b)=>String(a.webkitRelativePath||a.name).localeCompare(String(b.webkitRelativePath||b.name),undefined,{numeric:true,sensitivity:'base'}));

  const form=new FormData();
  selected.forEach(f=>form.append('photos',f));
  form.append('relativePaths',JSON.stringify(selected.map(f=>f.webkitRelativePath||f.name)));
  const r=await fetch('/api/upload-photos',{method:'POST',body:form});
  const nuevas=await r.json();

  photos=[];
  photos.push(...nuevas.sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'})));
  render();
  analyzePhotos(nuevas);
}
'''
    s = s[:start] + block + s[end:]

html.write_text(s, encoding="utf-8")
