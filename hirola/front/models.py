from django.db import models
from django.shortcuts import render
from django.core.files.images import get_image_dimensions
from django.core.cache import cache
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


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

    def save(self, *args, **kwargs):
        cache.delete('landing_page_images')
        super(LandingPageImage, self).save(*args, **kwargs)


class PhoneCategoryList(models.Model):
    class Meta:
        verbose_name_plural = "Phone Categories"
    phone_category = models.CharField(default=None, max_length=15, blank=False,
                                      unique=True)

    def __str__(self):
        return self.phone_category

    def save(self, *args, **kwargs):
        cache.delete('phone_categories')
        if self.pk:
            cache.delete('category_{}'.format(self.pk))
        super(PhoneCategoryList, self).save(*args, **kwargs)


class PhoneMemorySize(models.Model):
    abbreviation = models.CharField(max_length=10)
    size_number = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(PhoneCategoryList,
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True)

    def __str__(self):
        return str(self.size_number) + " " + self.abbreviation

    def save(self, *args, **kwargs):
        if self.category:
            cache.delete('sizes_{}'.format(self.category.id))
            if self.pk:
                delete_cache(PhoneMemorySize, self.pk, 'sizes_{}')
        if self.pk and self.category is None:
            delete_cache(PhoneMemorySize, self.pk, 'sizes_{}')
        super(PhoneMemorySize, self).save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.pk and self.category is None:
            delete_cache(PhoneList, self.pk, 'phones_{}')
        if self.category:
            cache.delete('phones_{}'.format(self.category_id))
            if self.pk:
                delete_cache(PhoneList, self.pk, 'phones_{}')
        super(PhoneList, self).save(*args, **kwargs)


def delete_cache(model_class, object_id, cache_name):
    model_object = model_class.objects.get(pk=object_id)
    if model_object.category:
        cache.delete(cache_name.format(model_object.category.id))


@receiver(pre_delete, sender=LandingPageImage)
def clear_landing_page_cache(sender, **kwargs):
    cache.delete('landing_page_images')


@receiver(pre_delete, sender=PhoneCategoryList)
def clear_phone_categories_cache(sender, **kwargs):
    cache.delete('phone_categories')
    cache.delete("category_{}".format(kwargs["instance"].id))
    cache.delete("phones_{}".format(kwargs["instance"].id))
    cache.delete("sizes_{}".format(kwargs["instance"].id))


@receiver(pre_delete, sender=PhoneList)
def clear_phone_cache(sender, **kwargs):
    cache_delete("phones_{}", kwargs["instance"].category)


@receiver(pre_delete, sender=PhoneMemorySize)
def clear_phone_mem_size_cache(sender, **kwargs):
    cache_delete("sizes_{}", kwargs["instance"].category)


def cache_delete(cache_name, cache_id):
    if cache_id:
        cache.delete(cache_name.format(cache_id.id))
