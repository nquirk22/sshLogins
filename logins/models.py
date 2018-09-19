from django.db import models

class Fail(models.Model):
    initiated = models.DateTimeField(unique=True)
    login = models.CharField(max_length=20)
    ip = models.CharField(max_length=60)