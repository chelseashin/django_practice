from django.db import models

# Create your models here.
class Friend(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    birthday = models.DateField(auto_now_add=True)
    age = models.IntegerField()
    
def __str__(self):
    return f"{self.id} : {self.name}"