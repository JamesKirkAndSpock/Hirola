from django.db import models
from django.shortcuts import render
from django.core.files.images import get_image_dimensions


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
    carousel_color = models.CharField(default='red', max_length=10,
                                      choices=CAROUSEL_COLORS)
    phone_name = models.CharField(max_length=20, default='', blank=True)
    phone_tag = models.CharField(max_length=30, default='', blank=True)
    text_color = models.CharField(default='white', max_length=10,
                                  choices=TEXT_COLORS)


class PhoneCategoryList(models.Model):
    class Meta:
        verbose_name_plural = "Phone Categories"
    phone_category = models.CharField(default=None, max_length=15, blank=False,
                                      unique=True)

    def __str__(self):
        return self.phone_category


class PhoneMemorySize(models.Model):
    abbreviation = models.CharField(max_length=10)
    size_number = models.IntegerField(blank=True, null=True)
    size_category = models.ForeignKey(PhoneCategoryList,
                                      on_delete=models.SET_NULL, null=True,
                                      blank=True)

    def __str__(self):
        return str(self.size_number) + " " + self.abbreviation


class Currency(models.Model):
    class Meta:
        verbose_name_plural = "Currencies"
    currency_abbreviation = models.CharField(max_length=5)
    currency_long_form = models.CharField(max_length=15)

    def __str__(self):
        return str(self.currency_abbreviation)


class PhoneList(models.Model):
    class Meta:
        verbose_name_plural = "Phones"
    category = models.ForeignKey(PhoneCategoryList, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    phone_image = models.ImageField()
    phone_name = models.CharField(max_length=20, blank=False, default=None)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    size_sku = models.ForeignKey(PhoneMemorySize, on_delete=models.SET_NULL,
                                 null=True, blank=True)
