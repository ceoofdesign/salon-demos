"""Fill _template/index.html from a JSON spec: python3 _template/fill.py spec.json
spec keys: slug, vars{PLACEHOLDER: value}, css (signature styles), root (replacement :root primitives block, optional),
signature_html (inserted at the hero SIGNATURE marker), after_hero_html (section inserted before #usluge, optional).
"""
import json, re, sys, pathlib
base = pathlib.Path(__file__).resolve().parent
spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
html = (base / "index.html").read_text()
html = re.sub(r"<!--\s*\n\s*БАЗОВЫЙ.*?-->\n", "", html, flags=re.S)
if spec.get("root"):
    html = re.sub(r"/\* primitives.*?\*/\n.*?(?=\s*/\* semantic)", spec["root"], html, count=1, flags=re.S)
html = html.replace("/* SIGNATURE: стили фишки салона сюда */", spec.get("css", ""))
html = html.replace("<!-- SIGNATURE: фишка салона (полоска дней, печать, слайдер и т. п.) -->", spec.get("signature_html", ""))
html = html.replace("<!-- герой смотрит в сторону текста; при фото слева поменять порядок колонок -->\n", "")
if spec.get("after_hero_html"):
    html = html.replace('<main>\n', '<main>\n' + spec["after_hero_html"] + "\n", 1)
for k, v in spec["vars"].items():
    html = html.replace("{{" + k + "}}", v)
for a, b in spec.get("replace", []):
    html = html.replace(a, b)
left = re.findall(r"\{\{\w+\}\}", html)
if left:
    sys.exit("unfilled: " + ", ".join(sorted(set(left))))
out = base.parent / spec["slug"] / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print("wrote", out)
