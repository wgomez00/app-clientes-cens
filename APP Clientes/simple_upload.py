from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = p.read_text(encoding="utf-8")
start = s.find("async function analyzePhotos")
end = s.find("async function upload", start)
if start >= 0 and end >= 0:
    s = s[:start] + s[end:]

old = '''  render();
  analyzePhotos(nuevas);
}
function collect()'''
new = '''  render();
}
function collect()'''
s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
