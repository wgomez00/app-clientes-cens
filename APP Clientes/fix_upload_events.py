from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
start=s.find("drop.onclick=()=>input.click();")
end=s.find("async function upload(files){",start)
if start>=0 and end>=0:
    events='''drop.onclick=()=>input.click();
input.onchange=e=>{ if(e.target.files?.length) upload(e.target.files); };
['dragenter','dragover'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.add('drag')}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.remove('drag')}));
drop.addEventListener('drop',async e=>{
  e.preventDefault();
  const items=[...(e.dataTransfer?.items||[])];
  const entries=items.map(item=>item.webkitGetAsEntry?.()).filter(Boolean);
  if(!entries.length){ upload(e.dataTransfer.files); return; }
  const files=[];
  async function readEntry(entry,path=''){
    if(entry.isFile){
      const file=await new Promise(resolve=>entry.file(resolve));
      Object.defineProperty(file,'webkitRelativePath',{value:path+file.name,configurable:true});
      files.push(file);
    }else if(entry.isDirectory){
      const reader=entry.createReader();
      const children=await new Promise(resolve=>reader.readEntries(resolve));
      for(const child of children) await readEntry(child,path+entry.name+'/');
    }
  }
  for(const entry of entries) await readEntry(entry);
  upload(files);
});
'''
    s=s[:start]+events+s[end:]
p.write_text(s,encoding="utf-8")
