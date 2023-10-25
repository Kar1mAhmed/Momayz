from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from locations.models import Area

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,username, password):
        user = self.create_user(
            username=username,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ]

class User(AbstractBaseUser):
    email= models.EmailField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=11, unique=True)
    gender =models.CharField(max_length=20, choices=GENDER_CHOICES)
    city = models.ForeignKey(Area, on_delete=models.PROTECT, null=True, blank=True)
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    img = models.CharField(max_length=100, blank=True, null=True)
    
    notification_token = models.CharField(max_length=255)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'username' 

    REQUIRED_FIELDS = []

    objects = MyUserManager()

    
    def deduct_credits(self, amount):
        if self.credits >= amount:
            self.credits -= amount
            self.save(update_fields=['credits'])
            return True  # Deduction successful
        else:
            raise ValueError('No enough credits.')
        
    def refund_credits(self, amount):
        self.credits += amount
        self.save(update_fields=['credits'])
        return True
    
    def __str__(self):
        return  self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True