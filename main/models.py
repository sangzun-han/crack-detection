from django.db import models

# Create your models here.


class Photo(models.Model):
    image = models.ImageField(upload_to='images/', null=False)
    flatting_image = models.ImageField(upload_to='flatting/', null=True)
    origin_width = models.FloatField(null=True)
    origin_height = models.FloatField(null=True)
    
    def __str__(self):
        return str(self.id)
