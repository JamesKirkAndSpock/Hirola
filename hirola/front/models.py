from django.db import models
from django.shortcuts import render
from django.core.files.images import get_image_dimensions

# Create your models here.
class LandingPageImage(models.Model):
    CAROUSEL_COLORS = (
        ('red', 'red'),
        ('amber', 'amber'),
        ('green', 'green'),
    )
    TEXT_COLORS = (
        ('white', 'white'),
        ('black', 'black'),
    )
    photo = models.ImageField()
    carousel_color = models.CharField(default='red', max_length=10, choices=CAROUSEL_COLORS)
    phone_name = models.CharField(max_length=20, default='', blank=True)
    phone_tag = models.CharField(max_length=30, default='', blank=True)
    text_color = models.CharField(default='white', max_length=10, choices=TEXT_COLORS)