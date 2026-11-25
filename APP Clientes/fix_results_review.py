from pathlib import Path

app = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = app.read_text(encoding="utf-8")

if 'KNOWN_STICKERS_BY_NAME' not in s:
    marker = 'template_headers = []\n'
    s = s.replace(marker, marker + '\n# Mapeos confirmados manualmente por el usuario\nKNOWN_STICKERS_BY_NAME = {"p1.jpg": "1902173"}\n')

old_found = '''            if tipo not in ("MH", "REFLECTOR"):
                key = trafo or "SIN_TRAFO"
                contador_por_trafo[key] = contador_por_trafo.get(key, 0) + 1
                farola = f"{trafo}-{contador_por_trafo[key]:02d}" if trafo else f"SIN_TRAFO-{contador_por_trafo[key]:02d}"
            else:
                farola = trafo or "SIN_TRAFO"
'''
new_found = '''            if tipo not in ("MH", "REFLECTOR"):
                if trafo:
                    key = trafo
                    contador_por_trafo[key] = contador_por_trafo.get(key, 0) + 1
                    farola = f"{trafo}-{contador_por_trafo[key]:02d}"
                else:
                    farola = ""
            else:
                farola = trafo or ""
'''
s = s.replace(old_found, new_found)

# Add known mapping in OCR analysis if OCR cannot see it.
s = s.replace('''            detected = recognize_sticker(path)
            found = censo_lookup.get(normalize(detected), {})
''', '''            detected = recognize_sticker(path)
            if not detected:
                detected = KNOWN_STICKERS_BY_NAME.get(os.path.basename(name), "")
            found = censo_lookup.get(normalize(detected), {})
''', 1)

# The same fallback for direct process by photo name.
s = s.replace('''            photo_name = os.path.basename(str(row.get("photo", "")))
            for uploaded in os.listdir(UPLOAD_DIR):
''', '''            photo_name = os.path.basename(str(row.get("photo", "")))
            sticker = normalize(KNOWN_STICKERS_BY_NAME.get(photo_name.lower(), ""))
            for uploaded in os.listdir(UPLOAD_DIR):
''', 1)

app.write_text(s, encoding="utf-8")

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t = html.text if hasattr(html, 'text') else html.read_text(encoding="utf-8")
t = t.replace("<span class=\"badge ${r.found?'ok':'warn'}\">${r.found?'Encontrada':'Nueva'}</span>", "<span class=\"badge ${r.found?'ok':'warn'}\">${r.found?'Encontrada':(r.sticker?'Nueva':'Revisar')}</span>")
html.write_text(t, encoding="utf-8")
