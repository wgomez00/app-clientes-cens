from pathlib import Path

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = html.read_text(encoding="utf-8")
old = '''  const seleccionados=[...files].filter(f=>/\\.(jpg|jpeg)$/i.test(f.name));
'''
new = '''  const vistos=new Set();
  const seleccionados=[...files].filter(f=>{
    const nombre=f.name.trim().toLowerCase();
    if(nombre==='p13.jpg'||nombre==='p15.jpg')return false;
    if(/n\\s*[_\\/-]*\\s*a/i.test(nombre)||/\\bna\\b/i.test(nombre)||nombre.includes('na.'))return false;
    const punto=nombre.match(/^p(\\d+)\\.(jpg|jpeg)$/i);
    const clave=punto?`p${parseInt(punto[1],10)}`:nombre;
    if(vistos.has(clave))return false;
    vistos.add(clave);
    return /\\.(jpg|jpeg)$/i.test(nombre);
  });
'''
if old in s:
    s = s.replace(old, new)
html.write_text(s, encoding="utf-8")

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
t = app.read_text(encoding="utf-8")
old_upload = '''        if file and file.filename:
'''
new_upload = '''        if file and file.filename:
            nombre_original = file.filename.strip().lower()
            if nombre_original in ('p13.jpg','p15.jpg'):
                continue
            if 'n/a' in nombre_original or 'n_a' in nombre_original or 'n-a' in nombre_original:
                continue
'''
t = t.replace(old_upload, new_upload, 1)
app.write_text(t, encoding="utf-8")
