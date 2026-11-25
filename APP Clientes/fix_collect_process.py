from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = p.read_text(encoding="utf-8")
start = s.find("function collect(){")
end = s.find("document.getElementById('process').onclick", start)
if start >= 0 and end >= 0:
    new = '''function collect(){
  const cards=[...document.querySelectorAll('.photo')];
  return cards.map((card,i)=>{
    const base=photos[i];
    return {
      photo:base.name,
      sticker:card.querySelector('.sticker')?.value||base.sticker||'',
      tipo:card.querySelector('.tipo')?.value||base.tecnologia||'LED',
      potencia:card.querySelector('.potencia')?.value||base.potencia||'',
      farola:card.querySelector('.farola')?.value||base.farola||'',
      trafo:'',
      municipio:document.getElementById('municipio').value,
      ubicacion:document.getElementById('ubicacion').value,
      fecha:document.getElementById('fecha').value,
      clasificacion:document.getElementById('clasificacion').value,
      observaciones:document.getElementById('observaciones').value
    };
  });
}
'''
    s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8")
