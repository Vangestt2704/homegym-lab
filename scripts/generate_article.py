#!/usr/bin/env python3
import os, csv, argparse, datetime, random, json

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA = os.path.join(ROOT, "data", "topics.csv")
ART_DIR = os.path.join(ROOT, "site", "articles")
PUB_LOG = os.path.join(ROOT, "data", "published.json")

os.makedirs(ART_DIR, exist_ok=True)

def load_published():
    if os.path.exists(PUB_LOG):
        return json.load(open(PUB_LOG, "r", encoding="utf-8"))
    return {"slugs": []}

def save_published(d):
    json.dump(d, open(PUB_LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def render_html(row):
    title = row["title"]
    slug = row["slug"]
    kws = row["keywords"]
    angle = row["angle"]
    asins = [a.strip() for a in row["asins"].split("|") if a.strip()]
    date = datetime.date.today().isoformat()

    def affiliate_box(asins):
        if not asins:
            return ""
        items = "".join([f'<li><a rel="sponsored noopener" href="https://www.amazon.fr/dp/{a}?tag=VOTRETAG-21" target="_blank">Voir le produit {i+1}</a></li>' for i,a in enumerate(asins)])
        return f"""
        <div class="card">
          <h3>Suggestions rapides</h3>
          <ul>{items}</ul>
          <p class="meta">Liens affiliés Amazon — à personnaliser avec votre tag.</p>
        </div>"""

    intro = f"""{title} — Dans ce guide, on passe en revue l'essentiel pour t'aider à décider rapidement, sans blabla inutile."""

    sections = f"""
    <div class="card">
      <h2>{title}</h2>
      <p class="meta">Publié le {date} • Mots-clés : {kws}</p>
      <p>{intro}</p>
    </div>
    <div class="card">
      <h3>1) Points-clés en 30 secondes</h3>
      <ul>
        <li>À qui ça s'adresse : {angle}.</li>
        <li>Budget: entrée, milieu, premium — choisis selon l'usage réel.</li>
        <li>Place disponible: vérifie dimensions et charge au sol.</li>
        <li>Sécurité: stabilité, serrage, garanties constructeur.</li>
      </ul>
    </div>
    <div class="card">
      <h3>2) Erreurs fréquentes à éviter</h3>
      <ul>
        <li>Se fier uniquement au prix « le plus bas ».</li>
        <li>Oublier les accessoires essentiels (sangles, tapis, colliers).</li>
        <li>Ignorer l'entretien (lubrification, contrôles de serrage).</li>
      </ul>
    </div>
    <div class="card">
      <h3>3) Notre mini-checklist</h3>
      <ul>
        <li>Objectif: force, muscle ou cardio ?</li>
        <li>Fréquence d'entraînement: 2–5×/semaine.</li>
        <li>Espace: <code>longueur × largeur × hauteur</code>.</li>
        <li>Charge utile nécessaire aujourd'hui + marge 20%.</li>
      </ul>
    </div>
    {affiliate_box(asins)}
    <div class="card">
      <h3>FAQ rapide</h3>
      <p><b>Combien investir ?</b> Commence petit, upgrade au besoin — mieux vaut la constance que le matériel parfait.</p>
      <p><b>Quels muscles ciblés ?</b> Dépend de l'exercice : traction, développé, squat, hip hinge, gainage.</p>
      <p><b>Entretien ?</b> Nettoyage, lubrification légère, contrôle des boulons 1×/mois.</p>
    </div>
    <div class="notice">Avertissement: toujours respecter les consignes de sécurité et s'échauffer correctement.</div>
    """

    html = f"""<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Home Gym Lab</title>
<meta name="description" content="{title} : guide rapide, erreurs à éviter, checklist et FAQ.">
<link rel="stylesheet" href="/assets/styles.css">
</head><body>
<header class="site-header"><h1>Home Gym Lab</h1>
<nav><a href="/">Accueil</a> • <a href="/outils/">Outils</a> • <a href="/a-propos.html">À propos</a></nav></header>
<main>
{sections}
</main><footer><p>© {datetime.date.today().year} Home Gym Lab • <a href="/">Accueil</a></p></footer></body></html>
"""
    return html, slug

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=5, help="How many new articles to generate")
    args = ap.parse_args()
    published = load_published()
    slugs_done = set(published.get("slugs", []))

    rows = list(csv.DictReader(open(DATA, "r", encoding="utf-8")))
    todo = [r for r in rows if r["slug"] not in slugs_done]
    random.shuffle(todo)
    created = 0
    for row in todo[:args.count]:
        html, slug = render_html(row)
        out = os.path.join(ART_DIR, f"{slug}.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        slugs_done.add(slug)
        created += 1

    published["slugs"] = list(slugs_done)
    save_published(published)
    print(f"Generated {created} article(s).")

if __name__ == "__main__":
    main()
