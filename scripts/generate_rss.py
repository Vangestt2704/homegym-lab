#!/usr/bin/env python3
import os, glob, datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE = "https://homegym-lab.pages.dev"

items = []
for html in sorted(glob.glob(os.path.join(ROOT, "site", "articles", "*.html")), reverse=True)[:20]:
    slug = os.path.basename(html).replace(".html","")
    with open(html, "r", encoding="utf-8") as f:
        txt = f.read()
    t1 = txt.find("<h2>"); t2 = txt.find("</h2>", t1+1)
    title = txt[t1+4:t2].strip() if t1!=-1 and t2!=-1 else slug
    items.append((title, slug))

rss = ['<?xml version="1.0" encoding="UTF-8" ?>',
       '<rss version="2.0"><channel>',
       f'<title>Home Gym Lab</title>',
       f'<link>{BASE}/</link>',
       f'<description>Guides Home Gym</description>',
       f'<lastBuildDate>{datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>']
for title, slug in items:
    rss.append(f"<item><title>{title}</title><link>{BASE}/articles/{slug}.html</link></item>")
rss.append("</channel></rss>")

with open(os.path.join(ROOT, "site", "feed.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(rss))
print("feed.xml generated (remember to set BASE).")
