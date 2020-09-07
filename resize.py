import os
from PIL import Image

img_path = r"C:\Users\HEDGE PENSIONS TRUST\Desktop\clones\Dj\wintrust2\app\static\app\images\news-letter.jpg"

img = Image.open(img_path)
print(img.width)
print(img.height)
img = img.resize((600,300))
img.save(r"C:\Users\HEDGE PENSIONS TRUST\Desktop\clones\Dj\wintrust2\app\static\app\images\news-letter.jpg")