from pathlib import Path

p=Path(r"C:\MDEsmart\APP Clientes\app.py")
s=p.read_text(encoding="utf-8")
start=s.find('@app.route("/api/upload-photos"')
end=s.find('@app.route("/api/analyze-photo"',start)
if start>=0 and end>=0:
    new='''@app.route("/api/upload-photos", methods=["POST"])
def upload_photos():
    saved=[]
    import json
    try:
        relative_paths=json.loads(request.form.get("relativePaths","[]"))
    except Exception:
        relative_paths=[]

    files=request.files.getlist("photos")
    by_point={}
    for index,file in enumerate(files):
        if not file or not file.filename:
            continue
        name=(relative_paths[index] if index < len(relative_paths) else file.filename).strip()
        lower=name.lower()
        if lower in ("p13.jpg","p15.jpg"):
            continue
        if "n/a" in lower or "n_a" in lower or "n-a" in lower or lower.startswith("na."):
            continue
        match=re.match(r"^p(\\d+)\\.(jpg|jpeg)$",lower)
        if not match:
            continue
        point=int(match.group(1))
        if point in by_point:
            continue
        by_point[point]=file

    for point in sorted(by_point):
        file=by_point[point]
        name=f"p{point}.jpg"
        filename=f"{len(os.listdir(UPLOAD_DIR)):05d}_{name}"
        path=os.path.join(UPLOAD_DIR,filename)
        file.save(path)
        saved.append({"name":name,"url":f"/uploads/{filename}","sticker":"","farola":"","potencia":"","municipio":"","trafo":"","tecnologia":"LED","ubicacion":""})
    return jsonify(saved)

'''
    s=s[:start]+new+s[end:]
p.write_text(s,encoding="utf-8")
