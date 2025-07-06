from django.db import models

class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title
    
class Color(models.Model):
    title = models.CharField(max_length=20) 

    def __str__(self):
        return self.title   

class Product(models.Model):
    title = models.CharField(max_length=50)
    description =models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField()
    image = models.ImageField(upload_to='products')
    size =models.ManyToManyField("Size", related_name='products')
    color = models.ManyToManyField("Color", related_name='products')

    def __str__(self):
        return self.title