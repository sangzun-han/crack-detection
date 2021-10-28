from django.db import models

# Create your models here.


class Photo(models.Model):
    image = models.ImageField(upload_to='images/', null=False)
    flatting_image = models.ImageField(upload_to='flatting/', null=True)
    length_image = models.ImageField(upload_to='length/', null=True)
    area_image = models.ImageField(upload_to='area/', null=True)
    
    def __str__(self):
        return str(self.id)
