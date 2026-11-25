from pathlib import Path

path = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
text = path.read_text(encoding="utf-8")
old = "drop.addEventListener('drop',e=>{e.preventDefault();upload(e.dataTransfer.files)});"
new = """drop.addEventListener('drop',async e=>{
  e.preventDefault();
  const items=[...(e.dataTransfer?.items||[])];
  const entries=items.map(item=>item.webkitGetAsEntry?.()).filter(Boolean);
  if(entries.length){
    const files=[];
    async function readEntry(entry,path=''){
      if(entry.isFile){
        const file=await new Promise(resolve=>entry.file(resolve));
        Object.defineProperty(file,'webkitRelativePath',{value:path+file.name,configurable:true});
        files.push(file);
      }else if(entry.isDirectory){
        const reader=entry.createReader();
        let children=[];
        do{
          const batch=await new Promise(resolve=>reader.readEntries(resolve));
          children=children.concat(batch);
          if(batch.length){};
          if(!batch.length) break;
        }while(true);
        for(const child of children) await readEntry(child,path+entry.name+'/');
      }
    }
    for(const entry of entries) await readEntry(entry);
    upload(files);
  }else{
    upload(e.dataTransfer.files);
  }
});"""
if old not in text:
    raise SystemExit("No se encontró el manejador original")
path.write_text(text.replace(old,new),encoding="utf-8")
