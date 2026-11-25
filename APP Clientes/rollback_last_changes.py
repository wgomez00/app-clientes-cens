from pathlib import Path
p=Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace('''      <div class="drop" id="drop">Arrastra aquí las fotos JPG<br><small>o usa los botones siguientes</small></div>
      <input id="photos" type="file" accept=".jpg,.jpeg,image/jpeg" multiple hidden>
      <button class="secondary" id="selectPhotos" style="width:100%;margin-top:8px">Seleccionar fotos JPG</button>
''','''      <div class="drop" id="drop">Arrastra aquí cualquier carpeta de fotos<br><small>o haz clic y selecciona una carpeta completa</small></div>
      <input id="photos" type="file" accept=".jpg,.jpeg,image/jpeg" multiple hidden>
''')
s=s.replace("document.getElementById('selectPhotos').onclick=()=>input.click();\n","")
p.write_text(s,encoding="utf-8")
