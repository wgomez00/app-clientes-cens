from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
start=s.find("const drop=document.getElementById('drop')")
if start>=0:
    end=s.find("function collect(){",start)
    if end>=0:
        block='''const drop=document.getElementById('drop'), input=document.getElementById('photos'), list=document.getElementById('photosList');
let photos=[], resultRows=[];
function esc(v){return String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
function photoCard(p,i){return `<div class="photo"><img src="${esc(p.url)}" alt="Foto"><div class="photo-body"><strong>${esc(p.name)}</strong><div class="mini-grid"><label>Código sticker<input class="sticker" data-i="${i}" value="${esc(p.sticker||'')}" placeholder="Ej. 1900679"></label><label>Potencia<input class="potencia" data-i="${i}" value="${esc(p.potencia||'')}" placeholder="Ej. 35"></label><label>Tecnología<select class="tipo" data-i="${i}"><option LED>LED</option><option MH>MH</option><option SODIO>SODIO</option></select></label><label>Farola<input class="farola" data-i="${i}" value="${esc(p.farola||'')}" readonly></label></div></div></div>`}
function render(){list.innerHTML=photos.length?photos.map(photoCard).join(''):`<div class="empty">Aún no hay fotos cargadas</div>`}
async function subirArchivos(files){
  const seleccionados=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name));
  if(!seleccionados.length){alert('Selecciona archivos JPG');return;}
  const form=new FormData();
  seleccionados.forEach(f=>form.append('photos',f));
  form.append('relativePaths',JSON.stringify(seleccionados.map(f=>f.name)));
  const r=await fetch('/api/upload-photos',{method:'POST',body:form});
  if(!r.ok){alert('Error al cargar las fotos');return;}
  const data=await r.json();
  photos=data;
  render();
}
drop.onclick=()=>input.click();
input.onchange=e=>subirArchivos(e.target.files);
['dragenter','dragover'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.add('drag')}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.remove('drag')}));
drop.ondrop=e=>{e.preventDefault();subirArchivos(e.dataTransfer.files);};
'''
        s=s[:start]+block+s[end:]
p.write_text(s,encoding="utf-8")
