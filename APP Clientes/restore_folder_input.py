from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace('accept=".jpg,.jpeg,image/jpeg" multiple hidden', 'accept=".jpg,.jpeg,image/jpeg" multiple webkitdirectory directory hidden')
p.write_text(s,encoding="utf-8")
