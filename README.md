# Home Gym Lab — Micro‑média automatisé (gratuit)

**Ce repo contient tout le nécessaire** pour publier automatiquement des articles (site statique) et générer des Shorts YouTube (artefacts).
Aucun abonnement requis. Héberge le site gratuitement avec **Cloudflare Pages** et programme la publication via **GitHub Actions**.

## Déploiement rapide
1. Crée un repo GitHub privé (ou public) et uploade tous les fichiers de ce dossier.
2. Active **Actions** (onglet *Actions* → *I understand my workflows...*).
3. Dans **Settings → Actions → General → Workflow permissions**, coche **Read and write permissions** (pour autoriser le commit auto).
4. Va dans **Actions** et lance le workflow manuellement (*Run workflow*) pour tester.
5. Crée un projet **Cloudflare Pages** relié à ce repo. Build command: _aucune_, Output directory: `site`.
6. Remplace dans `site/sitemap.xml` et `site/feed.xml` la valeur `https://YOUR-DOMAIN.pages.dev` après le premier déploiement.

## Contenu & automatisation
- `data/topics.csv` : 240 sujets (longue traîne). Le workflow publie **5 nouveaux articles/jour** par défaut.
- `scripts/generate_article.py` : génère les pages `/site/articles/*.html`.
- `scripts/build_index.py` : régénère la liste d'accueil.
- `scripts/generate_sitemap.py` & `scripts/generate_rss.py` : SEO de base.
- `scripts/shorts_from_csv.py` : génère 1 Short/jour (1080x1920, 8s) avec **ffmpeg + eSpeak** (aucun service externe). Les vidéos sont sauvegardées en artefacts du workflow pour les récupérer et publier sur YouTube (upload auto possible ultérieurement).

## Monétisation (0€)
- **AdSense** : ajoute ton code d'annonce dans `site/partials/adsense.html` (placeholder) *une fois accepté*.
- **Amazon** : remplace `VOTRETAG-21` par ton tag dans `scripts/generate_article.py` (fonction affiliate_box).

## Ajustements utiles
- Pour publier plus/moins d'articles : modifie `--count` dans le workflow YAML.
- Pour accélérer l'indexation : crée un compte Google Search Console et soumets `/sitemap.xml`.
- Pour personnaliser le style : édite `site/assets/styles.css` et le header.
- Pour changer de niche : modifie `data/topics.csv`.

## Avertissements
- Le contenu généré est générique; enrichis progressivement (photos perso, conseils, tests).
- Respecte les politiques des plateformes (AdSense, YouTube, Amazon).
