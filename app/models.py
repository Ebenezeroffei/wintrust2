from django.db import models
from django.contrib.auth.models import User
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
        """ This function changes the resolution of the image before saving it """
        super().save()
        images = [self.image1,self.image2,self.image3]
        for img in images:
            new_img = Image.open(img.path)
            if img.width > 500 or img.height > 500:
                new_img= new_img.resize((500,500))
                new_img.save(img.path)
    
    def active_images(self):
        """ This function returns all the active images in the product """
        return [img for img in [self.image1,self.image2,self.image3] if img]
        
                
    def __str__(self):
        return f"{self.name}"


class Cart(models.Model):
    """ This stores the table for the users cart """
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItems(models.Model):
    """ This is responsible for recording the items in the users cart """
    cart = models.ForeignKey(Cart,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.SmallIntegerField(default = 1)
    
    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s Cart"

class NewsLetters(models.Model):
    """ This model stores all the emails that will be used to send newsletters """
    email = models.EmailField()
    
class BillingAddress(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    company_name = models.CharField('Company Name (Optional)',max_length = 100,null = True,blank = True)
    state_or_country = models.CharField("State/Country",max_length = 100)
    town_or_city = models.CharField("Town/City",max_length = 100)
    phone = models.CharField(max_length = 50)
    email = models.EmailField()
    post_or_zipcode = models.CharField("Postcode/ZIP",max_length = 50)
    
    def _str_(self):
        return f"{self.user.username}'s Billing Address"
    
    