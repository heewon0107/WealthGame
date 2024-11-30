from django.db import models

# Create your models here.
class Exchange(models.Model):
    result = models.IntegerField()
    cur_unit = models.TextField()
    cur_nm = models.TextField()
    ttb = models.TextField()
    tts = models.TextField()