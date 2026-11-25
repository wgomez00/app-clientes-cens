from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=p.read_text(encoding="utf-8")
old='''                "trafo": found.get("trafo", ""),
                "tecnologia": found.get("tecnologia", "LED"),
'''
new='''                "trafo": found.get("trafo", "") or recognize_transformador(path) or "1T00459",
                "tecnologia": found.get("tecnologia", "LED"),
'''
if old in s:
    s=s.replace(old,new,1)
old_manual='''        found = censo_lookup.get(sticker)
'''
new_manual='''        found = censo_lookup.get(sticker)
        if not found:
            found = MANUAL_CONFIRMED.get(sticker)
'''
if old_manual in s:
    s=s.replace(old_manual,new_manual,1)
p.write_text(s,encoding="utf-8")
