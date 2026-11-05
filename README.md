# 15081-assignment1
## introduction
<p>Organic Care is a showcase website model based on HTML and CSS. Creates for Assignment of LIBRARIES, TOOLS & WORKFLOW CRN-15081-202401.</p>
<br>

## Material
<p>All image material was downloaded from freepik.com and AI tools.</p>

## Product catalogue

Serve the static site from this directory with `python3 -m http.server 8000`.
`products.html` links to nine individual product pages. The catalogue and detail
pages use bundled Bootstrap styles, so their layout does not require a CDN.

Edit product names, descriptions, ingredients, benefits, sizes, or image paths in
`catalogue.json`, then run `python3 tools/generate_catalogue.py` to regenerate the
listing and all detail pages. Run the generator after changing shared catalogue
header/footer markup so those changes reach the detail pages as well.

This is a sample catalogue, with illustrative ingredients and sizes; it does not
process orders or payments.
