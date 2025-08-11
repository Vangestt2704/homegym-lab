#!/usr/bin/env python3
import os, glob, datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE = "https://homegym-lab.pages.dev"
paths = ["/", "/outils/", "/a-propos.html", "/feed.xml"]
for html in glob.glob(os.path.join(ROOT, "site", "articles", "*.html")):
    paths.append("/articles/" + os.path.basename(html))

xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
today = datetime.date.today().isoformat()
for p in paths:
    xml.append(f"<url><loc>{BASE}{p}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq></url>")
xml.append("</urlset>")

with open(os.path.join(ROOT, "site", "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("sitemap.xml generated (remember to set BASE).")
