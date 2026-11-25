from pathlib import Path
p = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = p.read_text(encoding="utf-8")
old = "    if(nombre.includes('thumb') || nombre.includes('mini') || nombre.includes('preview')) continue;"
new = "    if(nombre.includes('thumb') || nombre.includes('mini') || nombre.includes('preview') || nombre.includes('..')) continue;"
if old not in s:
    raise SystemExit("Filtro no encontrado")
p.write_text(s.replace(old,new), encoding="utf-8")
