"""Regenerate static catalogue pages from catalogue.json. Run from any directory."""
import json
import re
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / 'catalogue.json').read_text())
listing = (ROOT / 'products.html').read_text()
# The existing listing supplies the shared header/footer and three-column layout.
head = listing[:listing.index('    <main>')]
footer = listing[listing.index('    <footer>'):listing.index('    </footer>') + len('    </footer>\n')]
for network in ('facebook', 'instagram', 'youtube'):
 footer = footer.replace(f'class="fa fa-{network}" style="font-size:24px"></a>', f'>{network.title()}</a>')
head = re.sub(r'    <!--AOS animation links-->.*?<title>.*?</title>', '    <title>Products | Organic Care</title>', head, flags=re.S)
head = re.sub(r'    <link href="https://cdn.jsdelivr.net/.*?crossorigin="anonymous">', '    <link rel="stylesheet" href="./node_modules/bootstrap/dist/css/bootstrap.min.css">', head, flags=re.S)
head = re.sub(r'    <link rel="stylesheet" href="https://cdnjs[^\n]+\n', '', head)
head = head.replace("<i class='fas fa-shopping-cart' style='font-size:1.2em'></i>", 'Checkout')
head = head.replace('<ul>\n                <li>', '<ul>\n                <li><a href="./index.html">Home</a></li>\n                <li>', 1) if '>Home</a>' not in head else head
cover = listing[listing.index('    <main>'):listing.index('        <div class="container')]
sections = []
for category in dict.fromkeys(p['category'] for p in products):
 slug = category.lower().replace(' ', '-')
 cards = []
 for p in products:
  if p['category'] != category: continue
  cards.append(f'''                <div class="col col-12 col-md">
                    <a class="product-card" href="./{p['id']}.html">
                        <img src="./{p['image']}" alt="{e(p['name'])}" loading="lazy">
                        <p>{e(p['name'])}</p>
                    </a>
                </div>''')
 sections.append(f'''        <div class="container catalogue-category" id="{slug}">
            <div class="seemorebox"><h3>{category}</h3></div>
            <div class="row">
{chr(10).join(cards)}
            </div>
        </div>''')
(ROOT / 'products.html').write_text(head + cover + '\n'.join(sections) + '\n    </main>\n' + footer + '</body>\n</html>\n')
for p in products:
 slug = p['category'].lower().replace(' ', '-')
 benefits = ''.join(f'<li>{e(b)}</li>' for b in p['benefits'])
 related = ''.join(f'''<a class="related-card" href="./{q['id']}.html"><img src="./{q['image']}" alt="{e(q['name'])}" loading="lazy"><h3>{e(q['name'])}</h3><p>{e(q['size'])}</p><span>View product →</span></a>''' for q in products if q['category']==p['category'] and q!=p)
 pagehead = head.replace('Products | Organic Care', e(p['name']) + ' | Organic Care').replace('</head>', f'    <meta name="description" content="{e(p["description"])}">\n    <link rel="stylesheet" href="./product-detail.css">\n</head>')
 (ROOT / (p['id']+'.html')).write_text(pagehead + f'''
    <main class="product-detail">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="./products.html">Products</a><span aria-hidden="true">/</span><a href="./products.html#{slug}">{e(p['category'])}</a><span aria-hidden="true">/</span><span aria-current="page">{e(p['name'])}</span></nav>
        <article class="product-overview">
            <img class="product-photo" src="./{p['image']}" alt="{e(p['name'])}">
            <div class="product-copy">
                <p class="eyebrow">Organic Care · {e(p['category'])}</p>
                <h1>{e(p['name'])}</h1>
                <p class="ingredients">{e(p['ingredients'])}</p>
                <p class="product-description">{e(p['description'])}</p>
                <ul class="benefits" aria-label="Benefits">{benefits}</ul>
                <dl class="product-specs"><div><dt>Skin type</dt><dd>{e(p['category'])}</dd></div><div><dt>Size</dt><dd>{e(p['size'])}</dd></div></dl>
                <a class="browse-button" href="./products.html#{slug}">Explore {e(p['category'].lower())} care <span aria-hidden="true">→</span></a>
                <p class="sample-note">Sample product catalogue. Ingredients and sizes are illustrative.</p>
            </div>
        </article>
        <section class="related-products" aria-labelledby="related-heading"><div class="related-heading"><h2 id="related-heading">More for {e(p['category'].lower())}</h2><a href="./products.html#{slug}">See all →</a></div><div class="related-grid">{related}</div></section>
    </main>
''' + footer + '</body>\n</html>\n')
print(f'Generated catalogue and {len(products)} product detail pages.')
