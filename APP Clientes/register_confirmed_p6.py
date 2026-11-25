from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=p.read_text(encoding="utf-8")
marker='censo_lookup = {}\n'
extra='''MANUAL_CONFIRMED = {
    "1935920": {
        "municipio": "CUCUTA",
        "cuadrante": "",
        "longitud": "",
        "latitud": "",
        "potencia": "35",
        "farola": "1553529",
        "trafo": "",
        "tecnologia": "LED",
    }
}

'''
if 'MANUAL_CONFIRMED =' not in s:
    s=s.replace(marker,marker+extra)
s=s.replace('''        found = censo_lookup.get(sticker)
''','''        found = censo_lookup.get(sticker)
        if not found:
            found = MANUAL_CONFIRMED.get(sticker)
''',1)
p.write_text(s,encoding="utf-8")
