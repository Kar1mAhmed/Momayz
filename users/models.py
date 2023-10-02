from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ]

class User(AbstractBaseUser):
    email= models.EmailField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    gender =models.CharField(max_length=20, choices=GENDER_CHOICES)
    govern = models.CharField(max_length=50)
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    img = models.SmallIntegerField()
    
    notification_token = models.CharField(max_length=255)
    with_facebook = models.BooleanField(default=False, blank=True)
    with_google = models.BooleanField(default=False, blank=True)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email' 

    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return  self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True