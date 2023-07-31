from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
from django.utils.translation import activate
from PIL import Image


# Create your models here.



class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Email field is required')

        if not password:
            raise ValueError('Password is required')

        if not username:
            raise ValueError('Username is required')

        user_obj = self.model(username=username,email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self,username,email,password=None):
        user = self.create_user(username,email,password=password,is_staff=True)
        return user
    
    def create_superuser(self,username,email,password=None):
        user = self.create_user(username,email,password=password,is_staff=True,is_admin=True)
        return user

class User(AbstractBaseUser):
    username           =     models.CharField(max_length=100,unique=True)
    email              =     models.EmailField(max_length=255,unique=True)
    image              =     models.ImageField(blank=True,default='profile_pics/default.jpg',upload_to="profile_pics")
    is_active          =     models.BooleanField(default=True)
    staff              =     models.BooleanField(default=False)
    admin              =     models.BooleanField(default=False)
    timestamp          =     models.DateTimeField(default=timezone.now)
    is_administrator   =     models.BooleanField(default=False)
    is_hall_manager    =     models.BooleanField(default=False)
    is_customer        =     models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']


    objects = UserManager()


    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin

    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)  # saving image first

        img = Image.open(self.image.path) # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)


class Administrator(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.user.username}"
    
class HallManager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    phone_number    = models.CharField(max_length=12,default='03214123882')

    def __str__(self):
        return f"{self.user.username}"


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}"

    
