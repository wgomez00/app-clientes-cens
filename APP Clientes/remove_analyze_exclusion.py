from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=p.read_text(encoding="utf-8")
block='''            if should_exclude_photo(path):
                return jsonify({"name": name, "excluded": True, "sticker": "", "farola": "", "potencia": "", "municipio": "", "trafo": "", "tecnologia": "", "ubicacion": ""})
'''
s=s.replace(block,'')
p.write_text(s,encoding="utf-8")
