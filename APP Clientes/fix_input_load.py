from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = p.read_text(encoding="utf-8")
s = s.replace('<input id="photos" type="file" accept=".jpg,.jpeg,image/jpeg" multiple webkitdirectory directory hidden>', '<input id="photos" type="file" accept=".jpg,.jpeg,image/jpeg" multiple hidden>')
s = s.replace("drop.onclick=()=>input.click();", "drop.onclick=()=>input.click();")
p.write_text(s, encoding="utf-8")
