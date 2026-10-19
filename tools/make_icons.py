"""Generates the app icons (web + Android) from code, so they stay reproducible."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SKY, GRASS, RED, BLUE, WHITE = '#7cc8ff', '#74c66b', '#e2392b', '#2f7ff0', 'white'

def tiles(dr, n, scale=1.0, off=0):
    s = n * scale
    def box(x0, y0, w, fill, ch, rot):
        tile = Image.new('RGBA', (int(w), int(w)), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.rounded_rectangle([0, 0, w - 1, w - 1], radius=int(w * .22), fill=fill)
        td.text((w / 2, w / 2 + w * .02), ch, font=ImageFont.truetype(FONT, int(w * .62)), fill=WHITE, anchor='mm')
        return tile.rotate(rot, resample=Image.BICUBIC, expand=True), (x0, y0)
    w = s * .46
    a, pa = box(off + s * .12, off + s * .16, w, RED, 'А', 8)
    b, pb = box(off + s * .44, off + s * .38, w, BLUE, 'B', -8)
    return [(a, pa), (b, pb)]

def full(n):
    im = Image.new('RGBA', (n, n), SKY)
    dr = ImageDraw.Draw(im)
    dr.ellipse([-n * .3, n * .72, n * 1.3, n * 1.5], fill=GRASS)
    for t, p in tiles(dr, n):
        im.alpha_composite(t, (int(p[0]), int(p[1])))
    return im.convert('RGB')

def round_mask(im):
    n = im.size[0]
    m = Image.new('L', (n, n), 0); ImageDraw.Draw(m).ellipse([0, 0, n - 1, n - 1], fill=255)
    out = Image.new('RGBA', (n, n), (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

def foreground(n):
    # adaptive icon foreground: content kept inside the central 66% safe zone
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    inner = n * .62; off = (n - inner) / 2
    for t, p in tiles(None, inner):
        im.alpha_composite(t, (int(p[0] + off - inner * .02), int(p[1] + off - inner * .04)))
    return im

def main():
    d = os.path.join(ROOT, 'docs')
    for n, name in ((512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')):
        full(n).save(os.path.join(d, name))
    full(512).save(os.path.join(ROOT, 'store', 'icon-512.png')) if os.path.isdir(os.path.join(ROOT, 'store')) else None
    res = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'res')
    if os.path.isdir(res):
        for dens, n in (('mdpi', 48), ('hdpi', 72), ('xhdpi', 96), ('xxhdpi', 144), ('xxxhdpi', 192)):
            p = os.path.join(res, 'mipmap-' + dens); os.makedirs(p, exist_ok=True)
            full(n).save(os.path.join(p, 'ic_launcher.png'))
            round_mask(full(n)).save(os.path.join(p, 'ic_launcher_round.png'))
            foreground(int(n * 2.25)).save(os.path.join(p, 'ic_launcher_foreground.png'))
        import glob
        for f in glob.glob(os.path.join(res, 'drawable*', 'splash.png')):
            w, h = Image.open(f).size
            im = Image.new('RGBA', (w, h), '#dff3ff')
            ImageDraw.Draw(im).ellipse([-w * .3, h * .78, w * 1.3, h * 1.6], fill=GRASS)
            n = int(min(w, h) * .42)
            im.alpha_composite(round_mask(full(n)), ((w - n) // 2, (h - n) // 2))
            im.convert('RGB').save(f)
    print('icons ok')

if __name__ == '__main__':
    main()
