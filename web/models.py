from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


user_group, created = Group.objects.get_or_create(name='Users')
admin_group, created = Group.objects.get_or_create(name='Administrators')
class Phone(models.Model):
    os = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    details = models.TextField()
    photo = models.ImageField(upload_to='phones/', null=True, blank=True)

    def __str__(self):
        return self.name
class Rating(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
class OS(models.Model):
    OSused = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    Manufacturer = models.CharField(max_length=50)
    category = models.ForeignKey(OS, on_delete=models.CASCADE)

    def __str__(self):
        return self.name