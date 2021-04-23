from django.db import models

from django.contrib.auth.models import User

class CsvFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return self.file.name
