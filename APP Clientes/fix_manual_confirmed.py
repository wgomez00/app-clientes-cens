from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=p.read_text(encoding="utf-8")
start=s.find("def load_excels():")
manual_start=s.find("MANUAL_CONFIRMED =", start)
if start>=0:
    before=s[:start]
    manual='''MANUAL_CONFIRMED = {
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
    # Remove misplaced manual block and keep load_excels from the end.
    rest=s[start:]
    rest=rest.replace('''def load_excels():
    global censo_lookup, municipio_contracto, template_headers
MANUAL_CONFIRMED = {
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

    censo_lookup = {}
''','''def load_excels():
    global censo_lookup, municipio_contracto, template_headers
    censo_lookup = {}
''')
    s=before+manual+rest
p.write_text(s,encoding="utf-8")
