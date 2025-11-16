import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter

# Carica immagine originale in RGBA
img = np.array(Image.open("./223100.png").convert("RGBA"))
h, w, _ = img.shape

pad = 128
new_h, new_w = h + 2*pad, w + 2*pad
new = np.zeros((new_h, new_w, 4), dtype=np.uint8)

# Inserisci immagine al centro
new[pad:pad+h, pad:pad+w] = img

# ---- ANGOLI e BORDI (come da tua correzione) ----
corners = {
    "tl": img[0,0],
    "tr": img[0,-1],
    "bl": img[-1,0],
    "br": img[-1,-1]
}

# Bordi top/bottom
for x in range(w):
    top = img[0, x]
    bot = img[-1, x]
    for dy in range(pad):
        a = 255 - (255*dy)//pad
        new[pad-1-dy, pad+x] = [*top[:3], a]
        new[pad+h+dy, pad+x] = [*bot[:3], a]

# Bordi left/right
for y in range(h):
    left = img[y, 0]
    right = img[y, -1]
    for dx in range(pad):
        a = 255 - (255*dx)//pad
        new[pad+y, pad-1-dx] = [*left[:3], a]
        new[pad+y, pad+w+dx] = [*right[:3], a]

# Angoli
for dy in range(pad):
    for dx in range(pad):
        a = 255 - int(255 * (max(dx, dy) / pad))
        new[pad-dy, pad-dx]     = [*corners["tl"][:3], a]
        new[pad-dy, pad+w+dx]   = [*corners["tr"][:3], a]
        new[pad+h+dy, pad-dx]   = [*corners["bl"][:3], a]
        new[pad+h+dy, pad+w+dx] = [*corners["br"][:3], a]

# ---- BLUR 7x7 SUL PADDING+2 ----
mask = np.ones((new_h, new_w), dtype=bool)
mask[pad-2:pad+h+2, pad-2:pad+w+2] = False  # escluso img +2
blurred = uniform_filter(new.astype(float), size=(7,7,1))

# Applica blur solo sulle zone di padding
new[mask] = blurred[mask].astype(np.uint8)

# Salva risultato
Image.fromarray(new, mode="RGBA").save("output_blur_2.png")
