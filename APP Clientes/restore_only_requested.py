from pathlib import Path

html = Path(r"C:\MDEsmart\APP Clientes\app\templates\index.html")
s = html.read_text(encoding="utf-8")

old_input = '      <input id="photos" type="file" accept=".jpg,.jpeg,image/jpeg" multiple hidden>\n'
if old_input not in s:
    old_input = '      <input id="photos" type="file" accept=".jpg,.jpeg,image/jpeg" multiple hidden>'
new_input = '      <input id="photos" type="file" accept=".jpg,.jpeg,image/jpeg" multiple hidden>\n'
s = s.replace(old_input, new_input)

# Keep the original simple onchange behavior.
start = s.find("input.onchange=")
end = s.find("['dragenter','dragover']", start)
if start >= 0 and end >= 0:
    simple = '''input.onchange=e=>{ if(e.target.files?.length) upload(e.target.files); };
'''
    s = s[:start] + simple + s[end:]

html.write_text(s, encoding="utf-8")
