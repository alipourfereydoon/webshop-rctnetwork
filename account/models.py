from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    fullname = models.CharField(max_length=50 , verbose_name='نام کامل')
    phone = models.CharField(max_length=12,unique=True,verbose_name='شماره تماس')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural =' کاربران'

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
class Otp(models.Model):
    token = models.CharField(max_length=200 , null=True)
    phone = models.CharField(max_length=12) 
    code = models.IntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
    

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name='addresses')
    full_name= models.CharField(max_length=50)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=30)

    def __str__(self):
        return self.user.phone
    
class Contact(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(blank=True,null=True)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.fullname    
    
