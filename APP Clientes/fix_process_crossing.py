from pathlib import Path

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = app.read_text(encoding="utf-8")
old = '''    for row in rows:
        sticker = normalize(row.get("sticker", ""))
        found = censo_lookup.get(sticker)
'''
new = '''    for row in rows:
        sticker = normalize(row.get("sticker", ""))
        if not sticker:
            photo_name = os.path.basename(str(row.get("photo", "")))
            for uploaded in os.listdir(UPLOAD_DIR):
                if uploaded == photo_name or uploaded.endswith("_" + photo_name):
                    sticker = normalize(recognize_sticker(os.path.join(UPLOAD_DIR, uploaded)))
                    break
        found = censo_lookup.get(sticker)
'''
if old not in s:
    raise SystemExit("Bloque enrich no encontrado")
s = s.replace(old, new)

old_else = '''        else:
            municipio = str(row.get("municipio", "")).strip()
            longitud = str(row.get("longitud", "")).strip()
            latitud = str(row.get("latitud", "")).strip()
            potencia = potencia_foto
'''
new_else = '''        else:
            municipio = str(row.get("municipio", "")).strip()
            longitud = str(row.get("longitud", "")).strip()
            latitud = str(row.get("latitud", "")).strip()
            potencia = potencia_foto
'''
# Keep existing fallback but avoid generating fake values without an identified sticker.
app.write_text(s, encoding="utf-8")

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = html.read_text(encoding="utf-8")
t = t.replace("      farola:card.querySelector('.farola')?.value||base.farola||'',\n      trafo:'',", "      farola:card.querySelector('.farola')?.value||base.farola||'',\n      trafo:document.getElementById('transformador').value,")
html.write_text(t, encoding="utf-8")
