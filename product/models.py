from django.db import models

class Category(models.Model):
    parent = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE,related_name='subs')
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category,blank=True,null=True)
    title = models.CharField(max_length=50)
    description =models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField()
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.title
    
class Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE ,related_name='informations', null=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]
        

class Job(models.Model):
    # category = models.ManyToManyField(Category,blank=True,null=True)
    title = models.CharField(max_length=50)
    description =models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField()
    image = models.ImageField(upload_to='jobs')
    
    def __str__(self):
        return self.title
    
class Informationjob(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE ,related_name='informationjobs', null=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]        