from pathlib import Path

p = Path(r"C:\MDEsmart\APP Clientes\app.py")
s = p.read_text(encoding="utf-8")
old = '''            path = os.path.join(UPLOAD_DIR, filename)
            file.save(path)
            saved.append({"name": relative.replace("\\", "/"), "url": f"/uploads/{filename}"})
'''
new = '''            path = os.path.join(UPLOAD_DIR, filename)
            file.save(path)
            detected = recognize_sticker(path)
            found = censo_lookup.get(normalize(detected), {})
            saved.append({
                "name": relative.replace("\\", "/"),
                "url": f"/uploads/{filename}",
                "sticker": detected,
                "farola": found.get("farola", ""),
                "potencia": found.get("potencia", ""),
                "municipio": found.get("municipio", ""),
                "trafo": found.get("trafo", ""),
                "tecnologia": found.get("tecnologia", "LED"),
                "cuadrante": found.get("cuadrante", ""),
            })
'''
if old not in s:
    raise SystemExit("Endpoint no encontrado")
p.write_text(s.replace(old,new), encoding="utf-8")
