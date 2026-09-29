"""Fashion-illustration figures wearing each product (SVG, transparent background).

Style: elongated ~9-head croquis proportions, sculpted skin shading, soft fabric folds,
faceless head. Tops are framed head to mid-thigh, bottoms waist to feet, the set full length.
Run: python3 tools/draw_figures.py
"""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'images', 'products')
C = json.load(open(os.path.join(HERE, 'colors.json')))
C.update({'un-pant': '#9C9EA1', 'tt-session-7': '#1C8CCB', 'vu-seaside': '#5E4A46'})

SKIN, SKIN_DK, SKIN_HI, HAIR = '#6E432E', '#52301F', '#9A6A50', '#141010'
JOGGER, SHORTS_TAN, TEE_NEUTRAL = '#2A2B2E', '#BDAE9F', '#ECE8E1'


def hex2rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def rgb2hex(c): return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)
def mix(h, t, k):
    a, b = hex2rgb(h), hex2rgb(t)
    return rgb2hex([a[i] + (b[i] - a[i]) * k for i in range(3)])
def lum(h):
    r, g, b = (v / 255 for v in hex2rgb(h))
    return .2126 * r + .7152 * g + .0722 * b


class Pal:
    """Derived tones for one garment colour."""
    def __init__(self, c):
        self.c = c
        dark = lum(c) < .18
        self.dk = mix(c, '#000000', .25)
        self.in_ = mix(c, '#000000', .45)
        self.rib = mix(c, '#FFFFFF', .06) if dark else mix(c, '#000000', .1)
        self.edge = 'rgba(255,255,255,.16)' if dark else 'rgba(0,0,0,.2)'
        self.st = 'rgba(255,255,255,.24)' if dark else 'rgba(0,0,0,.24)'
        self.cord = mix(c, '#FFFFFF', .55 if dark else .35)
        self.fold_dk = 'rgba(0,0,0,.30)' if dark else 'rgba(0,0,0,.16)'
        self.fold_hi = 'rgba(255,255,255,.10)' if dark else 'rgba(255,255,255,.22)'
        self.noise = .16 if dark else .4


def fill(d, p):
    return (f'<path d="{d}" fill="{p.c}" stroke="{p.edge}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="url(#cloth)"/>')

def heather(d, p): return f'<path d="{d}" fill="#fff" filter="url(#nz)" opacity="{p.noise}"/>'
def rib(d, p): return f'<path d="{d}" fill="{p.rib}" stroke="{p.edge}" stroke-width="1"/>'
def seam(d, p, w=1.4): return f'<path d="{d}" fill="none" stroke="{p.edge}" stroke-width="{w}" stroke-linecap="round"/>'
def stitch(d, p): return f'<path d="{d}" fill="none" stroke="{p.st}" stroke-width="1.1" stroke-dasharray="3 3" stroke-linecap="round"/>'

def folds(clip_d, p, dark_lines, light_lines=()):
    """Soft blurred fold shading, clipped to the garment."""
    cid = 'f' + hashlib.md5(clip_d.encode()).hexdigest()[:8]
    s = f'<clipPath id="{cid}"><path d="{clip_d}"/></clipPath><g clip-path="url(#{cid})" filter="url(#soft)">'
    s += ''.join(f'<path d="{d}" fill="none" stroke="{p.fold_dk}" stroke-width="7" stroke-linecap="round"/>' for d in dark_lines)
    s += ''.join(f'<path d="{d}" fill="none" stroke="{p.fold_hi}" stroke-width="6" stroke-linecap="round"/>' for d in light_lines)
    return s + '</g>'

def cords(p, y0, y1, dark=False):
    col = '#1E1E1E' if dark else p.cord
    return (f'<circle cx="193" cy="{y0}" r="3" fill="{p.in_}" stroke="{p.cord}" stroke-width="1"/>'
            f'<circle cx="207" cy="{y0}" r="3" fill="{p.in_}" stroke="{p.cord}" stroke-width="1"/>'
            f'<path d="M193,{y0} C190,{y0 + 20} 188,{y1 - 20} 186,{y1}" stroke="{col}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
            f'<path d="M207,{y0} C210,{y0 + 20} 212,{y1 - 20} 214,{y1}" stroke="{col}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
            f'<rect x="183" y="{y1 - 2}" width="6" height="12" rx="2" fill="#2A2A2A"/>'
            f'<rect x="211" y="{y1 - 2}" width="6" height="12" rx="2" fill="#2A2A2A"/>')


# ---------- the figure (croquis: head 40-138, shoulders 186, waist 440, knee 700, ankle 900) ----------
def flip(d):
    """Mirror a path's x coordinates around x=200 (absolute commands, comma-separated pairs)."""
    res = []
    for t in d.split(' '):
        if ',' in t:
            head = ''
            while t and t[0].isalpha(): head, t = head + t[0], t[1:]
            x, y = t.split(',')
            res.append(f'{head}{400 - float(x):g},{y}')
        else:
            res.append(t)
    return ' '.join(res)

L_ARM = ('M112,184 C94,196 86,228 88,280 C90,328 84,362 82,394 C80,440 78,496 80,532 '
         'L102,534 C104,498 108,452 110,404 C112,364 118,324 124,292 C128,262 134,242 138,228 Z')
L_HAND = 'M80,528 C72,556 76,590 90,606 C100,608 106,590 104,560 L102,530 Z'
L_LEG = ('M150,436 C140,520 142,612 154,700 C146,760 150,826 166,902 L190,902 '
         'C192,842 198,782 191,730 C188,712 190,702 192,690 C197,602 201,540 201,480 Z')
TORSO = ('M182,168 L218,168 C240,178 270,178 292,188 C298,206 280,226 264,244 C262,300 260,342 258,382 '
         'C257,410 262,430 263,452 L137,452 C138,430 143,410 142,382 C140,342 138,300 136,244 '
         'C120,226 102,206 108,188 C130,178 160,178 182,168 Z')

def limb(d): return f'<path d="{d}" fill="{SKIN}"/><path d="{d}" fill="url(#skin)"/>'

def body_back():
    s = ''
    for d in (L_LEG, flip(L_LEG)): s += limb(d)
    for d in (L_ARM, flip(L_ARM), L_HAND, flip(L_HAND)): s += limb(d)
    s += limb(TORSO)
    # anatomy hints: knees, elbows, collarbones, sternum
    hint = f'fill="none" stroke="{SKIN_DK}" stroke-width="2" stroke-linecap="round" opacity=".55"'
    s += f'<path d="M160,698 C168,706 180,706 186,698 M240,698 C232,706 220,706 214,698" {hint}/>'
    s += f'<path d="M90,392 C96,398 104,398 108,392 M310,392 C304,398 296,398 292,392" {hint}/>'
    s += f'<path d="M150,196 C166,202 184,200 196,196 M250,196 C234,202 216,200 204,196" {hint}/>'
    s += f'<path d="M200,208 L200,300" {hint.replace('opacity=".55"', 'opacity=".3"')}/>'
    return s

def neck():
    d = 'M182,120 L218,120 C218,140 220,156 226,172 L174,172 C180,156 182,140 182,120 Z'
    return f'<path d="{d}" fill="{SKIN_DK}"/><path d="M186,150 C194,158 206,158 214,150" fill="none" stroke="#3E2416" stroke-width="3" opacity=".35" filter="url(#soft)"/>'

def head():
    face = 'M171,90 C171,58 184,44 200,44 C216,44 229,58 229,90 C229,114 217,134 200,138 C183,134 171,114 171,90 Z'
    s = f'<ellipse cx="170" cy="92" rx="5" ry="10" fill="{SKIN_DK}"/><ellipse cx="230" cy="92" rx="5" ry="10" fill="{SKIN_DK}"/>'
    s += f'<path d="{face}" fill="{SKIN}"/><path d="{face}" fill="url(#skin)"/>'
    s += f'<path d="M180,118 C188,132 212,132 220,118" fill="none" stroke="{SKIN_DK}" stroke-width="4" opacity=".35" filter="url(#soft)"/>'
    s += f'<path d="M171,84 C168,54 184,40 200,40 C216,40 232,54 229,84 C225,68 214,60 200,60 C186,60 175,68 171,84 Z" fill="{HAIR}"/>'
    return s

def shoes():
    L = 'M164,898 L192,898 L196,928 C196,942 150,946 144,938 C142,924 152,908 164,898 Z'
    s = ''
    for d in (L, flip(L)):
        s += f'<path d="{d}" fill="#F3F2EF" stroke="rgba(0,0,0,.2)" stroke-width="1.2"/>'
    s += '<path d="M144,934 C160,940 190,938 196,932 M256,934 C240,940 210,938 204,932" stroke="#D2CFC8" stroke-width="5" fill="none"/>'
    return s


# ---------- tops ----------
NECKS = {'crew': 'M178,170 C188,194 212,194 222,170', 'v': 'M178,172 L200,216 L222,172', 'polo': 'M178,170 L200,198 L222,170'}

def top_path(kind, hem=500, neck='crew'):
    nk = NECKS[neck]
    if kind == 'tee':
        r = ' C246,178 276,180 296,190 C308,200 316,230 320,290 L276,300 C272,280 268,262 264,246'
        l = 'C132,262 128,280 124,300 L80,290 C84,230 92,200 104,190 C124,180 154,178 178,170 Z'
    elif kind == 'long':
        r = (' C246,178 276,180 296,190 C310,202 316,240 314,290 C314,340 318,380 320,420 C322,460 322,500 322,532 '
             'L296,536 C294,500 292,460 290,420 C286,380 280,340 276,300 C272,280 268,262 264,246')
        l = ('C132,262 128,280 124,300 C120,340 114,380 110,420 C108,460 106,500 104,536 L78,532 '
             'C78,500 78,460 80,420 C82,380 86,340 86,290 C84,240 90,202 104,190 C124,180 154,178 178,170 Z')
    else:  # tank
        return (f'M178,170 C188,198 212,198 222,170 L240,172 C242,210 254,236 268,252 C266,330 266,420 264,{hem} '
                f'L136,{hem} C134,420 134,330 132,252 C146,236 158,210 160,172 Z')
    return nk + r + f' C266,330 266,420 264,{hem} L136,{hem} C134,420 134,330 136,246 ' + l

def top(kind, p, heather_on=False, neck_='crew', raglan=False, hem=500, extras=''):
    d = top_path(kind, hem, neck_)
    s = fill(d, p) + (heather(d, p) if heather_on else '')
    dark = ['M150,262 C156,330 154,400 158,' + str(hem), 'M250,262 C244,330 246,400 242,' + str(hem)]
    light = ['M186,230 C190,300 188,380 190,' + str(hem - 10)]
    if kind == 'long':
        dark += ['M96,330 C94,380 94,430 96,500', 'M304,330 C306,380 306,430 304,500']
    if hem > 470:
        dark.append(f'M150,{hem - 30} C180,{hem - 20} 220,{hem - 20} 250,{hem - 30}')
    s += folds(d, p, dark, light)
    if neck_ == 'crew':
        s += rib('M174,169 C186,199 214,199 226,169 L222,170 C212,192 188,192 178,170 Z', p)
    if kind in ('tee', 'long'):
        if raglan:
            s += seam('M184,178 C166,206 150,228 136,246', p) + seam('M216,178 C234,206 250,228 264,246', p)
        else:
            s += seam('M104,190 C116,212 128,230 136,246', p) + seam('M296,190 C284,212 272,230 264,246', p)
    if kind == 'tee':
        s += stitch('M84,280 L124,290', p) + stitch('M316,280 L276,290', p)
    if kind == 'long':
        s += rib('M78,532 L104,536 L105,514 L79,510 Z', p) + rib('M322,532 L296,536 L295,514 L321,510 Z', p)
    if kind == 'tank':
        s += stitch('M164,174 C162,212 150,236 138,250', p) + stitch('M236,174 C238,212 250,236 262,250', p)
    s += stitch(f'M138,{hem - 10} L262,{hem - 10}', p)
    return s + extras

def polo_bits(p):
    s = f'<path d="M188,172 L212,172 L200,198 Z" fill="{p.in_}"/>'
    s += rib('M193,192 L207,192 L207,258 L193,258 Z', p)
    s += ''.join(f'<circle cx="200" cy="{y}" r="3" fill="{mix(p.c, "#FFFFFF", .3)}" stroke="{p.edge}"/>' for y in (208, 228, 248))
    wing = 'M176,166 L190,162 L200,168 L200,198 L182,220 L166,182 Z'
    for w in (wing, flip(wing)):
        s += f'<path d="{w}" fill="{p.c}" stroke="{p.edge}" stroke-width="1.2" stroke-linejoin="round"/>'
    return s

def hood_back(p):
    return f'<path d="M146,198 C132,152 166,128 200,128 C234,128 268,152 254,198 L222,174 L200,218 L178,174 Z" fill="{p.dk}" stroke="{p.edge}" stroke-width="1.2"/>'

def hood_front(p, with_cords=True):
    s = f'<path d="M182,172 L218,172 L200,212 Z" fill="{p.in_}"/>' + seam('M178,174 L200,218 L222,174', p, 3)
    return s + (cords(p, 222, 292) if with_cords else '')

def pocket(p):
    return (rib('M156,400 L244,400 L258,490 L142,490 Z', p)
            + stitch('M160,406 L240,406', p) + stitch('M158,404 L146,484', p) + stitch('M242,404 L254,484', p))

def hem_band(p, y=472):
    s = rib(f'M136,{y} L264,{y} L264,500 L136,500 Z', p)
    return s + ''.join(seam(f'M{x},{y + 4} L{x},496', p, 1) for x in range(146, 264, 10))


# ---------- bottoms ----------
SHORTS = ('M146,440 L254,440 L258,470 C266,540 272,610 276,660 L208,668 L201,540 '
          'L199,540 L192,668 L124,660 C128,610 134,540 142,470 Z')
PANTS = ('M146,440 L254,440 L258,470 C266,600 258,780 246,900 L208,900 L201,550 '
         'L199,550 L192,900 L154,900 C142,780 134,600 142,470 Z')

def waistband(p): return rib('M146,440 L254,440 L258,470 L142,470 Z', p) + stitch('M147,448 L253,448', p) + stitch('M144,463 L256,463', p)

def shorts(p, heather_on=False, zip_pocket=False, perf=False, dark_cord=False, show_cords=True):
    s = fill(SHORTS, p) + (heather(SHORTS, p) if heather_on else '')
    s += folds(SHORTS, p, ['M196,540 C180,580 166,620 160,664', 'M204,540 C220,580 234,620 240,664'],
               ['M160,490 C156,560 150,610 146,650', 'M240,490 C244,560 250,610 254,650'])
    s += waistband(p) + seam('M200,470 L200,540', p) + stitch('M206,470 L206,506 C206,514 202,518 200,520', p)
    s += seam('M148,478 C154,500 156,516 158,530', p) + seam('M252,478 C246,500 244,516 242,530', p)
    s += stitch('M127,650 L191,658', p) + stitch('M273,650 L209,658', p)
    if zip_pocket:
        s += '<path d="M238,492 L241,548" stroke="#2A2A2A" stroke-width="2.2" stroke-linecap="round"/><rect x="236" y="544" width="8" height="14" rx="2" fill="#2A2A2A"/>'
    if perf:
        s += ''.join(f'<circle cx="{x + (y // 10 % 2) * 3}" cy="{y}" r="1.5" fill="{p.in_}"/>' for y in (570, 580, 590, 600, 610, 620, 630) for x in (254, 262))
    if show_cords: s += cords(p, 456, 530, dark_cord)
    return s

def pants(p, jogger=False, heather_on=False):
    s = fill(PANTS, p) + (heather(PANTS, p) if heather_on else '')
    s += folds(PANTS, p, ['M196,560 C186,640 180,720 176,780', 'M204,560 C214,640 220,720 224,780',
                          'M160,700 C168,712 180,712 188,704', 'M240,700 C232,712 220,712 212,704'],
               ['M160,500 C154,600 156,700 164,860', 'M240,500 C246,600 244,700 236,860'])
    s += waistband(p) + seam('M200,470 L200,550', p) + stitch('M208,470 L208,516 C208,526 203,530 200,532', p)
    s += seam('M148,476 C156,500 160,516 162,528', p) + seam('M252,476 C244,500 240,516 238,528', p)
    if jogger:
        s += rib('M154,872 L192,872 L192,900 L154,900 Z', p) + rib('M246,872 L208,872 L208,900 L246,900 Z', p)
        s += cords(p, 456, 520)
    else:
        s += ''.join(f'<rect x="{x}" y="437" width="7" height="36" rx="1" fill="{p.rib}" stroke="{p.edge}"/>' for x in (156, 180, 213, 237))
        s += f'<circle cx="200" cy="455" r="4" fill="{mix(p.c, "#FFFFFF", .25)}" stroke="{p.edge}"/>'
        s += stitch('M156,886 L192,886', p) + stitch('M244,886 L208,886', p)
    return s


# ---------- assemble ----------
FRAMES = {'top': '-44 28 488 610', 'bottom': '-20 400 440 550', 'full': '60 30 280 925'}

def svg(layers, frame='top'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{FRAMES[frame]}" role="img" aria-label="">
<defs>
  <linearGradient id="cloth" gradientUnits="userSpaceOnUse" x1="80" y1="0" x2="320" y2="60">
    <stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity=".2"/>
  </linearGradient>
  <linearGradient id="skin" x1="0" x2="1">
    <stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset=".32" stop-color="{SKIN_HI}" stop-opacity=".55"/>
    <stop offset=".5" stop-color="{SKIN_HI}" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/>
  </linearGradient>
  <filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3.5"/></filter>
  <filter id="nz" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="7"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 -.18"/>
    <feComposite in2="SourceAlpha" operator="in"/>
  </filter>
  <filter id="ds" x="-20%" y="-10%" width="140%" height="120%">
    <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#1A1714" flood-opacity=".16"/>
  </filter>
</defs>
<g filter="url(#ds)">
{layers}
</g>
</svg>
'''


def with_top(pid, kind, bottom='jogger', **kw):
    """A card for a top: the product over neutral bottoms."""
    p = Pal(C[pid])
    hood = kw.pop('hood', None)
    extras = ''
    if kw.pop('polo', False): extras += polo_bits(p)
    if kw.pop('band', False): extras += hem_band(p)
    if kw.pop('pocket', False): extras += pocket(p)
    if hood is not None: extras += hood_front(p, hood)
    s = body_back() + shoes()
    s += pants(Pal(JOGGER)) if bottom == 'jogger' else shorts(Pal(SHORTS_TAN), show_cords=False)
    s += (hood_back(p) if hood is not None else '') + neck()
    s += top(kind, p, **kw, extras=extras)
    return svg(s + head(), 'top')

def with_bottom(pid, kind, **kw):
    """A card for a bottom: the product under a neutral tee, tucked so the waistband shows."""
    p = Pal(C[pid])
    s = body_back() + shoes() + neck() + top('tee', Pal(TEE_NEUTRAL), hem=452)
    s += shorts(p, **kw) if kind == 'shorts' else pants(p, **kw)
    return svg(s + head(), 'bottom')

def set_figure():
    """The UNRL set: Ultra Tee over Stride Short, full length."""
    tee, sh = Pal(C['un-ultra']), Pal(C['un-stride'])
    s = body_back() + shoes() + shorts(sh, dark_cord=True, show_cords=False) + neck() + top('tee', tee, raglan=True)
    return svg(s + head(), 'full')


ART = {
    'tt-muscle': with_top('tt-muscle', 'tank', 'shorts', heather_on=True),
    'll-license': with_top('ll-license', 'long', 'shorts', neck_='v', raglan=True, hood=False),
    'lt-relax': with_top('lt-relax', 'long', band=True),
    'vu-strato-ls': with_top('vu-strato-ls', 'long', heather_on=True),
    'un-ultra': with_top('un-ultra', 'tee', raglan=True),
    'lt-supima': with_top('lt-supima', 'tee'),
    'vu-seaside': with_top('vu-seaside', 'long', 'shorts', neck_='v', band=True, pocket=True, hood=True),
    'rh-commuter': with_bottom('rh-commuter', 'pants'),
    'un-streamline': with_top('un-streamline', 'long', raglan=True, heather_on=True),
    'tt-session-lined': with_bottom('tt-session-lined', 'shorts', zip_pocket=True, perf=True),
    'un-stride': with_bottom('un-stride', 'shorts', dark_cord=True),
    'un-pant': with_bottom('un-pant', 'pants', jogger=True, heather_on=True),
    'ta-carrollton': with_top('ta-carrollton', 'long', neck_='v', heather_on=True, hood=True),
    'ta-cloud': with_top('ta-cloud', 'tee', neck_='polo', heather_on=True, polo=True),
    'vu-strato': with_top('vu-strato', 'tee', heather_on=True),
    'rh-regatta': with_top('rh-regatta', 'tee', neck_='polo', polo=True),
    'tt-session-7': with_bottom('tt-session-7', 'shorts'),
    'un-set': set_figure(),
}
if __name__ == '__main__':
    for pid, s in ART.items():
        open(os.path.join(OUT, pid + '.svg'), 'w').write(s)
    print(len(ART), 'written')
