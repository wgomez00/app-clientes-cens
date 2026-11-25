from pathlib import Path

app=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=app.read_text(encoding="utf-8")
marker='def normalize(value):\n'
func='''def normalize_tecnologia(value):
    text = str(value or "").strip().upper()
    compact = re.sub(r"[^A-Z0-9]", "", text)
    if "LDREFLEC" in compact or "LEDREFLECTOR" in compact:
        return "LED REFLECTOR"
    if "REFLEC" in compact:
        return "LED REFLECTOR"
    if compact in ("LD", "LED"):
        return "LED"
    if compact in ("NA", "SODIO"):
        return "SODIO"
    if compact in ("MH", "METAHADE", "METALAHADE", "METALHADIDO"):
        return "MH"
    return text or "LED"

'''
if 'def normalize_tecnologia' not in s:
    s=s.replace(marker,func+marker)
s=s.replace('tipo = str(row.get("tipo", "").upper())','tipo = normalize_tecnologia(row.get("tipo", ""))')
s=s.replace('tipo = str(row.get("tipo", "")).upper()','tipo = normalize_tecnologia(row.get("tipo", ""))')
app.write_text(s,encoding="utf-8")

html=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
t=html.read_text(encoding="utf-8")
t=t.replace('<option LED>LED</option><option MH>MH</option><option SODIO>SODIO</option>', '<option LED>LED</option><option MH>MH</option><option SODIO>SODIO</option><option LED REFLECTOR>LED REFLECTOR</option>')
html.write_text(t,encoding="utf-8")
