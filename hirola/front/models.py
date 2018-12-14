'''
Models
'''
from django.db import models
from django.core.cache import cache
from django.db.models.signals import pre_delete, post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class AreaCode(models.Model):
    '''
    Area code Numbers
    '''
    area_code = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "+" + str(self.area_code) + " " + self.country


class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email, password is not required.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, error_messages={
            'unique': _("The email address you entered has already been registered.",), },
                        max_length=255)
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_(
        'Designates whether the user can log into this admin site.'),)
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'), )
    is_change_allowed = models.BooleanField(_('change_allowed'), default=False, help_text=_(
            'Designates whether this user has been authorized to change his own'
            'password, in the change_password view.'),)
    area_code = models.ForeignKey(AreaCode, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    change_email = models.EmailField(_('email address'), unique=True, error_messages={
            'unique': _("The email address you entered has already been registered.",), },
                        max_length=255, default=None, blank=True, null=True)
    change_email_tracker = models.DateTimeField(_('change_email_tracker'), default=None, blank=True,
                                                null=True)
    former_email = models.EmailField(_('email address'), max_length=255, default=None, blank=True,
                                     null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # Require the email and password only
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        return self.email


class PhoneCategory(models.Model):
    class Meta:
        verbose_name_plural = "Phone Categories"
    phone_category = models.CharField(default=None, max_length=15, blank=False, unique=True)
    category_image = models.ImageField(blank=True, null=True, upload_to="phone_categories")

    def __str__(self):
        return self.phone_category

    def save(self, *args, **kwargs):
        cache.delete('phone_categories')
        if self.pk:
            cache.delete('category_{}'.format(self.pk))
        super(PhoneCategory, self).save(*args, **kwargs)


class PhoneMemorySize(models.Model):
    abbreviation = models.CharField(max_length=10)
    size_number = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(PhoneCategory, on_delete=models.SET_NULL, null=True, blank=True)

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


class ItemIcon(models.Model):
    item_icon = models.CharField(max_length=40)

    def __str__(self):
        return self.item_icon


class PhoneList(models.Model):
    class Meta:
        verbose_name_plural = "Phones"
    category = models.ForeignKey(PhoneCategory, on_delete=models.SET_NULL, null=True, blank=True)
    phone_name = models.CharField(max_length=20, blank=False, default=None)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    size_sku = models.ForeignKey(PhoneMemorySize, on_delete=models.SET_NULL, null=True, blank=True)
    icon = models.ForeignKey(ItemIcon, on_delete=models.SET_NULL, null=True, blank=True)
    average_review = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    main_image = models.ImageField(upload_to="phones")

    def __str__(self):
        return self.phone_name

    def save(self, *args, **kwargs):
        if self.pk and self.category is None:
            delete_cache(PhoneList, self.pk, 'phones_{}')
        if self.category:
            cache.delete('phones_{}'.format(self.category_id))
            if self.pk:
                delete_cache(PhoneList, self.pk, 'phones_{}')
        super(PhoneList, self).save(*args, **kwargs)


class SocialMedia(models.Model):
    class Meta:
        verbose_name_plural = "Social Media"
    url_link = models.URLField()
    icon = models.CharField(max_length=40, blank=True, default='')
    name = models.CharField(max_length=20, blank=False, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        cache.delete('social_media')
        super(SocialMedia, self).save(*args, **kwargs)


class OrderStatus(models.Model):
    status = models.CharField(max_length=20, blank=False, default=None)

    class Meta:
        verbose_name_plural = "Order Status'"

    def __str__(self):
        return self.status


class Order(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    phone = models.ForeignKey(PhoneList, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.phone) + ": " + str(self.owner) + " date: " + str(self.date)


class IntegerRangeField(models.IntegerField):

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Review(models.Model):
    stars = IntegerRangeField(min_value=1, max_value=5)
    comments = models.TextField()
    phone = models.ForeignKey(PhoneList,  related_name='phone_reviews', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.owner) + ": " + str(self.stars) + " stars: " + self.comments


class HotDeal(models.Model):
    item = models.ForeignKey(PhoneList, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.phone_name

    def save(self, *args, **kwargs):
        cache.delete('hot_deals')
        super(HotDeal, self).save(*args, **kwargs)


class PhoneImage(models.Model):
    phone = models.ForeignKey(PhoneList, related_name='phone_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="phones")


class Feature(models.Model):
    phone = models.ForeignKey(PhoneList, related_name='phone_features', on_delete=models.CASCADE)
    feature = models.TextField()


class ProductInformation(models.Model):
    phone = models.ForeignKey(PhoneList, related_name='phone_information', on_delete=models.CASCADE)
    feature = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


class NewsItem(models.Model):
    title = models.CharField(max_length=256)
    source = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    date_created = models.DateTimeField(_('date_created'), default=timezone.now)


def delete_cache(model_class, object_id, cache_name):
    model_object = model_class.objects.get(pk=object_id)
    if model_object.category:
        cache.delete(cache_name.format(model_object.category.id))


@receiver(pre_delete, sender=PhoneCategory)
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


@receiver(pre_delete, sender=SocialMedia)
def clear_social_media_cache(sender, **kwargs):
    cache.delete('social_media')


@receiver(pre_delete, sender=HotDeal)
def clear_hot_deals_cache(sender, **kwargs):
    cache.delete('hot_deals')


@receiver(post_save, sender=Review)
def adjust_average_review(sender, **kwargs):
    average_review(kwargs["instance"].phone_id)


@receiver(post_delete, sender=Review)
def adjust_average_review_delete(sender, **kwargs):
    average_review(kwargs["instance"].phone_id)


def average_review(phone_id):
    reviews = Review.objects.filter(phone=phone_id)
    if reviews:
        counter = 0
        for review in reviews:
            counter += review.stars
        average = counter / reviews.count()
        phone = PhoneList.objects.get(pk=phone_id)
        phone.average_review = average
        phone.save()
    else:
        phone = PhoneList.objects.get(pk=phone_id)
        phone.average_review = 5.0
        phone.save()


def cache_delete(cache_name, cache_id):
    if cache_id:
        cache.delete(cache_name.format(cache_id.id))
