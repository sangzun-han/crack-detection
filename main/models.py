from django.db import models

# Create your models here.


class Photo(models.Model):
    image = models.ImageField(upload_to='images/', null=False)
 
    def __str__(self):
        return self.id
