from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
from django.db import models

class UsrProfManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password=None, role='User'):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), full_name=full_name, phone=phone, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone, password):
        user = self.create_user(email, full_name, phone, password, role='Admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usr_prof(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=[('User', 'User'), ('Admin', 'Admin')])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    objects = UsrProfManager()

    def save(self, *args, **kwargs):
        """Ensure is_staff is set properly without affecting superusers"""
        if not self.is_superuser:  
            self.is_staff = self.role == 'Admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
class UserAdditionalInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Usr_prof, on_delete=models.CASCADE)
    extra_info = models.TextField()

    def __str__(self):
        return f"Additional Info for {self.user.full_name}"
    
class Movie(models.Model):

    GENRE_CHOICES = [
    ('action', 'Action'),
    ('comedy', 'Comedy'),
    ('drama', 'Drama'),
    ('horror', 'Horror'),
    ('sci-fi', 'Sci-Fi'),
    ('romance', 'Romance')
]
    name = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    GENRE= models.CharField(max_length=50, choices=GENRE_CHOICES)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()



    def __str__(self):
        return self.name

# Run migrations to create the table in MySQL:
# 1. python manage.py makemigrations
# 2. python manage.py migrate
# Create your models here.
