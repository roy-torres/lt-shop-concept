# Life Time Men's Edit — shop concept

A concept redesign of the men's apparel page on shop.lifetime.life. One static HTML file, no build step.

Concept by Roy Torres. Not affiliated with Life Time, Inc.

## What it does

- **Filter by activity.** The headline is the filter: tap Everything, Train, Run, Court, Basketball or Lifestyle.
- **Narrow further** by category (tops, bottoms, matching sets), brand, and price sort.
- **Search that understands shoppers.** "t-shirt", "sweatpants", "sleeveless", "tennis" or "vuori tee" all find the right pieces.
- **Quick add with your usual size.** Pick a size once and it's remembered for every other piece and for the matching set. The jogger uses waist sizes.
- **Bag drawer** with quantity and size changes, a free-shipping progress bar, and a bag that's saved on this device.
- Works on phones, in dark mode, with a keyboard, and with reduced motion.

## Run it

Open `index.html` in a browser. To serve it locally instead:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Files

```
index.html               the page: markup, styles and script
images/products/*.svg    one illustration per product, named by product id
tools/draw_figures.py    generates the illustrations
tools/colors.json        garment colours used by the generator
```

## Artwork

The product images are original SVG fashion illustrations, drawn in code. They aren't photos, and they contain no brand logos. To change them, edit `tools/draw_figures.py` and run it:

```sh
python3 tools/draw_figures.py
```

Tops are framed head to thigh, bottoms waist to feet, and the matching set full length.

## Content

Product names, brands and prices come from the Life Time men's apparel page as of 29 Sep 2026 and may have changed since. Brand names belong to their owners.

The typeface is [Archivo](https://fonts.google.com/specimen/Archivo) (SIL Open Font License), loaded from Google Fonts.
