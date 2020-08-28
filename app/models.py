from django.db import models
from PIL import Image

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 1000,decimal_places =2)
    description = models.CharField(max_length = 500)
    image1 = models.ImageField(upload_to = 'product_images/')
    image2 = models.ImageField(blank = True,null = True,upload_to = 'product_images/')
    image3 = models.ImageField(blank = True,null = True,upload_to = 'product_images/')
    
    def save(self):
        super().save()
        images = [self.image1,self.image2,self.image3]
        for img in images:
            new_img = Image.open(img.path)
            if img.width > 500 or img.height > 500:
                new_img= new_img.resize((500,500))
                new_img.save(img.path)
    
    def active_images(self):
        return [img for img in [self.image1,self.image2,self.image3] if img]
        
                
    def __str__(self):
        return f"{self.name}"