from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=p.read_text(encoding="utf-8")
old='''            for uploaded in os.listdir(UPLOAD_DIR):
                if uploaded == photo_name or uploaded.endswith("_" + photo_name):
                    sticker = normalize(recognize_sticker(os.path.join(UPLOAD_DIR, uploaded)))
                    break
'''
new='''            if not sticker:
                for uploaded in os.listdir(UPLOAD_DIR):
                    if uploaded == photo_name or uploaded.endswith("_" + photo_name):
                        sticker = normalize(recognize_sticker(os.path.join(UPLOAD_DIR, uploaded)))
                        break
'''
p.write_text(s.replace(old,new),encoding="utf-8")
