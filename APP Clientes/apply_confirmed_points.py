from pathlib import Path

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = app.read_text(encoding="utf-8")
start = s.find("KNOWN_STICKERS_BY_NAME =")
if start >= 0:
    end = s.find("\n", start)
    mapping = '{"p1.jpg":"1902173","p2.jpg":"1903903","p3.jpg":"1913922","p4.jpg":"1932636","p5.jpg":"1917445","p7.jpg":"1915660","p8.jpg":"1910410","p9.jpg":"1915645","p11.jpg":"1924068","p12.jpg":"1903289","p14.jpg":"1915650","p16.jpg":"1915687","p17.jpg":"1914630","p18.jpg":"1914094"}'
    s = s[:start] + 'KNOWN_STICKERS_BY_NAME = ' + mapping + s[end:]

# Force exclusion of points outside the circuit / without public lighting.
marker = 'def recognize_location(image_path):\n'
exclude_map = 'EXCLUDED_POINTS = {"p13.jpg", "p15.jpg"}\n\n'
if 'EXCLUDED_POINTS =' not in s:
    s = s.replace(marker, exclude_map + marker)

app.write_text(s, encoding="utf-8")

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = html.read_text(encoding="utf-8")
old = "const nombre=f.name.trim().toLowerCase();"
new = "const nombre=f.name.trim().toLowerCase();\n    if(nombre==='p13.jpg' || nombre==='p15.jpg') continue;"
if old in t:
    t = t.replace(old, new)
html.write_text(t, encoding="utf-8")
