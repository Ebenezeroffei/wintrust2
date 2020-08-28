from PIL import Image
import os

base_dir = r'C:\Users\HEDGE PENSIONS TRUST\Desktop\clones\Dj\wintrust2\app\static\app\images'
images = ['slide1.jpg','slide2.jpg','slide3.jpg','slide4.jpg','slide5.jpg']
count = 0
for img in images:
    img_path = os.path.join(base_dir,img)
    img =  Image.open(img_path)
#    print(img.width)
#    print(img.height)
#    print()
    img = img.resize((1500,550))
    img.save(fr'C:\Users\HEDGE PENSIONS TRUST\Desktop\clones\Dj\wintrust2\app\static\app\images\slide{count}(1).jpg')
    count += 1