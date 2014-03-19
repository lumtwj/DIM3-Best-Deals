from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User)
    address=models.CharField(max_length=120)
    handphone =models.CharField(max_length=120)
    postalcode = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

User.profile = property(lambda u:UserProfile.objects.get_or_create(user=u)[0])

class ProdRating(models.Model):
    productid = models.IntegerField()
    rate = models.FloatField(float,null=True)
    user_id_id = models.IntegerField()

class favouriteModel(models.Model):
    productid = models.IntegerField()
    productname = models.CharField(max_length=120)
    price = models.FloatField(float)
    website = models.CharField(max_length=120)
    image = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    user_id=models.IntegerField()
class productModel1(models.Model):
    productname = models.CharField(max_length=120)
    price = models.FloatField(float)
    website = models.CharField(max_length=120)
    image = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
class searchHistory(models.Model):
    user_id = models.CharField(max_length=120)
    keyword = models.CharField(max_length=120)
    date = models.CharField(max_length=120)