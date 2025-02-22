from django.db import models
from django.db import models

# Create your models here.
from django.db import models

class Usr_prof(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=[('User', 'User'), ('Admin', 'Admin')])  # ADD THIS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=
    255)
    
    def __str__(self):
        return self.full_name

class UserAdditionalInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Usr_prof, on_delete=models.CASCADE)
    extra_info = models.TextField()

    def __str__(self):
        return f"Additional Info for {self.user.full_name}"
    
class Movie(models.Model):
    name = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()

    def __str__(self):
        return self.name

# Run migrations to create the table in MySQL:
# 1. python manage.py makemigrations
# 2. python manage.py migrate
# Create your models here.
