from django.db import models
from django.contrib.auth.models import User


class Product ( models.Model ):
    name = models.CharField ( max_length=25 )
    price = models.IntegerField ()
    count = models.IntegerField ()
    description = models.TextField ()
    user = models.ForeignKey ( User, on_delete=models.CASCADE )


class Photo ( models.Model ):
    product = models.ForeignKey ( Product, on_delete=models.CASCADE,
                                  related_name="photo" )
    photo_url = models.ImageField ( upload_to="images" )


class Cart ( models.Model ):
    user = models.ForeignKey ( User, on_delete=models.CASCADE,
                               related_name="cart" )
    count = models.IntegerField ()
    product = models.ForeignKey ( Product, on_delete=models.CASCADE )


class Wish ( models.Model ):
    user = models.ForeignKey ( User, on_delete=models.CASCADE,
                               related_name="+" )
    product = models.ForeignKey ( Product, on_delete=models.CASCADE )


class Orders ( models.Model ):
    user = models.ForeignKey ( User, on_delete=models.CASCADE, )
    total = models.FloatField ()
    data = models.DateField ()


class OrderDatails ( models.Model ):
    order = models.ForeignKey ( Orders, on_delete=models.CASCADE, )
    product = models.ForeignKey ( Product, on_delete=models.CASCADE, )
    count = models.IntegerField ()
    feedback = models.TextField ()
# Create your models here.
