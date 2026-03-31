from PIL import Image
import os

SRC = '../processed'
DST = '../app/static/thumbs'

os.makedirs(DST, exist_ok=True)

for f in os.listdir(SRC):
    path = os.path.join(SRC, f)
    img = Image.open(path)
    img.thumbnail((300,300))
    img.save(os.path.join(DST, f))

print("Thumbnails generated")
