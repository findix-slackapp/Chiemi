from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Response(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

class Sorry(models.Model):
    answer = models.CharField(max_length=100)