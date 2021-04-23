from django.db import models

# Create your models here.

class Sample(models.Model):
    name = models.CharField(max_length=255)
    numero = models.IntegerField()

    def __str__(self):
        return self.name
