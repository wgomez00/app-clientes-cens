from pathlib import Path

html_path = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
html = html_path.read_text(encoding="utf-8")
html = html.replace("<label>Ubicación / Circuito</label><input id=\"ubicacion\" value=\"1T00459\" placeholder=\"Ej. 1T00459\">", "<label>Ubicación</label><input id=\"ubicacion\" value=\"1T00459\" placeholder=\"Ubicación del recorrido\">")
html = html.replace("const folderOriginal=document.getElementById('folderPath').value;\nconst partes=folderOriginal.split(/\\\\|\\//);\nconst posibleSeccion=partes.find(x=>/NIÑA|NINA|SECTOR|BARRIO/i.test(x));\nif(posibleSeccion) document.getElementById('ubicacion').value=posibleSeccion;", "document.getElementById('ubicacion').value='1T00459';")
html = html.replace("if(primero.trafo)document.getElementById('transformador').value=primero.trafo;", "if(primero.trafo)document.getElementById('transformador').value=primero.trafo;\n  if(primero.ubicacion)document.getElementById('ubicacion').value=primero.ubicacion;\n  if(!document.getElementById('ubicacion').value)document.getElementById('ubicacion').value='1T00459';")
html_path.write_text(html, encoding="utf-8")

app_path = Path(r"C:\MDEsmart\APP Clientes\app.py")
app = app_path.read_text(encoding="utf-8")
needle = '                            "tecnologia": row[ix.get("TEC. NUEVA", -1)] if ix.get("TEC. NUEVA", -1) >= 0 else "LED",\n'
replacement = needle + '                            "ubicacion": "1T00459",\n'
if needle in app:
    app = app.replace(needle, replacement, 1)
app_path.write_text(app, encoding="utf-8")
