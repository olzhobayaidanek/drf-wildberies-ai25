from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator,MinValueValidator


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(default=0)
    phone_number = PhoneNumberField(region='KG', default='+996')
    user_image = models.ImageField(upload_to='user_image/')
    CHOICES_STATUS =(
    ('gold','gold'),
    ('silver','silver'),
    ('bronze','bronze'),
    ('simple','simple')
    )

    status = models.CharField(choices=CHOICES_STATUS,default='simple')

    def __str__(self):
        return self.username





class Category(models.Model):
    category_name = models.CharField(max_length= 32, unique=True)

    def __str__(self):
        return self.category_name



class Subcategory(models.Model):
     category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_category')
     subcategory_name = models.CharField(max_length=32,unique=True)

     def __str__(self):
         return f'{self.category}: {self.subcategory_name }'




class Product(models.Model):
     category = models.ForeignKey(Category,on_delete=models.CASCADE)
     sub_category = models.ForeignKey(Subcategory,on_delete=models.CASCADE,related_name='sub_products')
     product_name = models.CharField(max_length=32)
     description = models.TextField(null=True,blank=True)
     price = models.DecimalField(max_digits=7, decimal_places=2)
     product_image = models.ImageField(upload_to='product_image/')

     def __str__(self):
         return f'{self.sub_category}: {self.product_name}'

     def get_avg_rating(self):
         reviews = self.reviews.all()
         if reviews.exists():
             return sum([i.stars for i in reviews]) / reviews.count()
         return 0

     def get_count_rating(self):
         reviews = self.reviews.all()
         if reviews.exists():
             return reviews.count()
         return 0

class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_product')
    image = models.ImageField(upload_to='image_product/')

class Review(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='reviews')
    images = models.ImageField(upload_to='review_images/', null=True,blank=True)
    video = models.FileField(upload_to='review_videos/', null=True,blank=True)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField(null=True,blank=True)

class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)

    def get_all_total_price(self):
        items = self.items.all()
        all_price =  float(sum([item.get_total_price()  for item in items]))
        discount = 0

        if self.user.status == 'gold':
            discount  = 0.70
        elif self.user.status == 'silver':
            discount = 0.50
        elif self.user.status == 'bronze':
            discount = 0.25


        finally_price = all_price * (1 - discount)
        return round(finally_price, 2)




class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

class Favorite(models.Model):
      user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite,on_delete=models.CASCADE,related_name='favorite_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

