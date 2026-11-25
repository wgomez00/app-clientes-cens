from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
# Replace input with a normal multi-file selector plus separate drop-folder support.
s=s.replace('accept=".jpg,.jpeg,image/jpeg" multiple hidden', 'accept=".jpg,.jpeg,image/jpeg" multiple hidden')
old='''drop.onclick=()=>input.click();
['dragenter','dragover'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.add('drag')}));'''
new='''drop.onclick=()=>input.click();
input.onchange=e=>upload(e.target.files);
['dragenter','dragover'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.add('drag')}));'''
s=s.replace(old,new)
s=s.replace("input.onchange=e=>upload(e.target.files);\n", "", 1)
p.write_text(s,encoding="utf-8")
