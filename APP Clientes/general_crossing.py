from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = p.read_text(encoding="utf-8")
s = s.replace('''                "tecnologia": found.get("tecnologia", "LED"),
                "ubicacion": "",
            })''', '''                "tecnologia": found.get("tecnologia", "LED"),
                "ubicacion": recognize_location(path),
            })''', 1)
p.write_text(s, encoding="utf-8")

h = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = h.read_text(encoding="utf-8")
old = '''          if(info.farola)card.querySelector('.farola').value=info.farola;
          if(info.tecnologia){'''
new = '''          if(info.farola)card.querySelector('.farola').value=info.farola;
          if(info.ubicacion)document.getElementById('ubicacion').value=info.ubicacion;
          if(info.municipio)document.getElementById('municipio').value=info.municipio;
          if(info.trafo)document.getElementById('transformador').value=info.trafo;
          if(info.tecnologia){'''
if old in t:
    t = t.replace(old, new)
h.write_text(t, encoding="utf-8")
