from pathlib import Path

p=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=p.read_text(encoding="utf-8")
needle='KNOWN_STICKERS_BY_NAME ='
start=s.find(needle)
if start>=0:
    end=s.find('\n',start)
    line=s[start:end]
    if 'p6.jpg' not in line:
        line=line.rstrip('}')+',"p6.jpg":"1935920","p10.jpg":"1901142"}'
    s=s[:start]+line+s[end:]
s=s.replace('PENDING_REVIEW = {"p6.jpg", "p10.jpg"}\n','')
p.write_text(s,encoding="utf-8")
