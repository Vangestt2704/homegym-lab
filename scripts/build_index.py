#!/usr/bin/env python3
import os, glob, datetime, json

ROOT = os.path.dirname(os.path.dirname(__file__))
ART_DIR = os.path.join(ROOT, "site", "articles")
INDEX = os.path.join(ROOT, "site", "index.html")

cards = []
for path in sorted(glob.glob(os.path.join(ART_DIR, "*.html"))):
    fname = os.path.basename(path)
    slug = fname.replace(".html","")
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    t1 = txt.find("<h2>"); t2 = txt.find("</h2>", t1+1)
    title = txt[t1+4:t2].strip() if t1!=-1 and t2!=-1 else slug
    cards.append({"title": title, "slug": slug})

with open(INDEX, "r", encoding="utf-8") as f:
    base = f.read()

cards_html = ["<div class='grid'>"]
for c in cards[::-1][:30]:
    cards_html.append(f"<div class='card'><h3><a href='/articles/{c['slug']}.html'>{c['title']}</a></h3><p class='meta'>Guide Home Gym</p></div>")
cards_html.append("</div>")
rendered = base.replace("<!-- build_index.py injecte ici la liste -->", "\n".join(cards_html))

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(rendered)

json_path = os.path.join(ROOT, "site", "feed.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({"updated": datetime.datetime.utcnow().isoformat()+"Z", "items": cards}, f, ensure_ascii=False, indent=2)

print(f"Index rebuilt with {len(cards)} article(s).")
