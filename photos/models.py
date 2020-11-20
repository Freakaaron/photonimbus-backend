from django.db import models

# Create your models here.


class Image(models.Model):
    """
        Summary of class goes here
    """
    username = models.CharField(max_length=20)
    image = models.BinaryField()
    thumbnail = models.BinaryField()

class SharedImage(models.Model):
    username = models.CharField(max_length=20)
    friend = models.CharField(max_length=20)
    image_id = models.TextField()

class Annotation(models.Model):
    username = models.CharField(max_length=20)
    image_id = models.TextField()
    annotation = models.TextField()