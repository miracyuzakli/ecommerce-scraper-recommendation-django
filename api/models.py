from django.db import models
from django.contrib.auth.models import User  # 

class Product(models.Model):
    category = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    rating_score = models.CharField(max_length=50)
    answered_questions = models.CharField(max_length=50)
    favorite = models.CharField(max_length=50, null=True, blank=True)
    feature_0 = models.CharField(max_length=255, null=True, blank=True)
    feature_1 = models.CharField(max_length=255, null=True, blank=True)
    feature_2 = models.CharField(max_length=255, null=True, blank=True)
    feature_3 = models.CharField(max_length=255, null=True, blank=True)
    feature_4 = models.CharField(max_length=255, null=True, blank=True)
    feature_5 = models.CharField(max_length=255, null=True, blank=True)
    feature_6 = models.CharField(max_length=255, null=True, blank=True)
    feature_7 = models.CharField(max_length=255, null=True, blank=True)
    image_name = models.CharField(max_length=255, null=True, blank=True)
    product_view = models.IntegerField(null=True, blank=True)

    
    def __str__(self):
        return self.product_name

class UserProductViewing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    user_viewing = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} Rating: {self.user_viewing}"
