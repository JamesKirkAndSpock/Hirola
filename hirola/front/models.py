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


def get_default():
    """
    Get the default country code.

    Returns:
        code(object): default country code
    """
    return CountryCode.objects.get_or_create(
        country_code=254, country="Kenya")[0]


class CountryCode(models.Model):
    '''
    Country code Numbers
    '''
    country_code = models.IntegerField(default=254, unique=True)
    country = models.CharField(max_length=255, default="Kenya", unique=True)

    def __str__(self):
        return "+" + str(self.country_code) + " " + self.country


class UserManager(BaseUserManager):
    """
    Interface for the User model for querying the database.
    """
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
        """
        Create a user with a default country code if none is provided.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not extra_fields.get('country_code'):
            extra_fields.setdefault('country_code', get_default())
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a proviledged user of the site
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if not extra_fields.get('country_code'):
            extra_fields.setdefault('country_code', get_default())

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Creates a user of the application."""
    email = models.EmailField(
        _('email address'), unique=True,
        error_messages={'unique': _(
            "The email address you entered has already been registered.",), },
        max_length=255
        )
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
            ),
        )
    is_active = models.BooleanField(
        _('active'), default=True, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'),
        )
    is_change_allowed = models.BooleanField(
        _('change_allowed'), default=False, help_text=_(
            'Designates whether this user has been authorized to change '
            'his own password, in the change_password view.'),
        )
    country_code = models.ForeignKey(CountryCode, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    change_email = models.EmailField(
        _('email address'), unique=True,
        error_messages={
            'unique': _(
                "The email address you entered has already been registered.",
                ),
            },
        max_length=255, default=None, blank=True, null=True
        )
    change_email_tracker = models.DateTimeField(_('change_email_tracker'),
                                                default=None, blank=True,
                                                null=True)
    former_email = models.EmailField(_('email address'), max_length=255,
                                     default=None, blank=True,
                                     null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # Require the email and password only
    REQUIRED_FIELDS = []

    def __str__(self):
        """Return a string representaion of the User object."""
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        return self.email


class InactiveUser(models.Model):
    email = models.EmailField(_('email address'), max_length=255)
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    country_code = models.ForeignKey(CountryCode, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    change_email = models.EmailField(
        _('email address'), max_length=255, default=None, blank=True,
        null=True)
    change_email_tracker = models.DateTimeField(
        _('change_email_tracker'), default=None, blank=True, null=True)
    former_email = models.EmailField(
        _('email address'), max_length=255, default=None, blank=True,
        null=True)
    password = models.CharField(max_length=100, default=None, blank=True,
                                null=True)

    def __str__(self):
        """Return a string representaion of the InactiveUser object."""
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        return self.email


class ItemIcon(models.Model):
    """Creates an Icon for phone models."""
    item_icon = models.CharField(max_length=50)

    def __str__(self):
        """Return a string representaion of the ItemIcon object."""
        return self.item_icon


class PhoneCategory(models.Model):
    """Creates Phone Categories."""

    class Meta:
        """Provides extra information for the model"""
        verbose_name_plural = "Phone Categories"
    phone_category = models.CharField(default=None, max_length=15, blank=False,
                                      unique=True)
    category_image = models.ImageField(blank=True, null=True,
                                       upload_to="phone_categories")
    category_icon = models.ForeignKey(ItemIcon, on_delete=models.SET_NULL,
                                      null=True, blank=True)

    def __str__(self):
        """Return a string representation of the PhoneCategory object."""
        return self.phone_category

    def save(self, *args, **kwargs):
        """Overrides the default save behavior of the model."""
        cache.delete('phone_categories')
        if self.pk:
            cache.delete('category_{}'.format(self.pk))
        super(PhoneCategory, self).save(*args, **kwargs)


class PhoneMemorySize(models.Model):
    """Creates Phone memory sizes."""
    abbreviation = models.CharField(max_length=10)
    size_number = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(PhoneCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    def __str__(self):
        return str(self.size_number) + " " + self.abbreviation

    def save(self, *args, **kwargs):
        """
        Overrides the default save behavior of the model and updates the
        cache.
        """
        if self.category:
            cache.delete('sizes_{}'.format(self.category.id))
            if self.pk:
                delete_cache(PhoneMemorySize, self.pk, 'sizes_{}')
        if self.pk and self.category is None:
            delete_cache(PhoneMemorySize, self.pk, 'sizes_{}')
        super(PhoneMemorySize, self).save(*args, **kwargs)


class Currency(models.Model):
    """Creates currencies."""
    class Meta:
        """
        Sets the plural name of the model which overrides the default name
        provided by django.
        """
        verbose_name_plural = "Currencies"
    currency_abbreviation = models.CharField(max_length=30)
    currency_long_form = models.CharField(max_length=50)

    def __str__(self):
        """Return a string representation of the Currency object."""
        return str(self.currency_abbreviation)


class SocialMedia(models.Model):
    """Creates Social media objects."""

    class Meta:
        """Sets the plural name of social media."""
        verbose_name_plural = "Social Media"
    url_link = models.URLField()
    icon = models.CharField(max_length=60, blank=True, default='')
    name = models.CharField(max_length=60, blank=False, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override default save behavior to enable updating of cache."""
        cache.delete('social_media')
        super(SocialMedia, self).save(*args, **kwargs)


class OrderStatus(models.Model):
    """Creates order status'"""

    status = models.CharField(max_length=60, blank=False, default=None)

    class Meta:
        """Sets the plural name of order status'"""
        verbose_name_plural = "Order Status'"

    def __str__(self):
        return self.status


class IntegerRangeField(models.IntegerField):
    """Defines custom behavior for the IntegerField."""

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, **kwargs)

    def formfield(self, **kwargs):
        """
        Sets default min and max values based on values provided by user.
        """
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class PaymentMethod(models.Model):
    """Creates payment methods."""
    payment_method = models.CharField(max_length=255, default="Cash")


class NewsItem(models.Model):
    """Creates news Items."""
    title = models.CharField(max_length=256)
    source = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    date_created = models.DateField(_('date_created'))

    def __str__(self):
        return str(self.link)


class Color(models.Model):
    """Creates colors for phones."""
    color = models.CharField(
        max_length=40, unique=True, error_messages={
            'unique': 'The color you entered already exists'})

    def __str__(self):
        return self.color


class Address(models.Model):
    """Creates addresses."""

    class Meta:
        """Override default plural name."""
        verbose_name_plural = "Addresses"

    address_line_one = models.CharField(max_length=255, null=False,
                                        blank=False)
    address_line_two = models.CharField(max_length=255, null=True,
                                        blank=True)
    short_description = models.CharField(max_length=255, null=True,
                                         blank=True)

    def __str__(self):
        if self.address_line_two:
            return self.address_line_one + '\n' + self.address_line_two
        return self.address_line_one


class ServicePerson(models.Model):
    """Creates service providers associated with the company."""

    class Meta:
        """Sets the plural name of the class to override the default name."""
        verbose_name_plural = "ServicePeople"

    first_name = models.CharField(max_length=30, null=False, blank=False)
    name_of_premise = models.CharField(max_length=255, null=False,
                                       blank=False)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                null=True, blank=True)
    country_code = models.ForeignKey(CountryCode, on_delete=models.SET_NULL,
                                     null=True, blank=False)
    phone_number = models.IntegerField(blank=False, null=False)
    msg = {'unique': _("The email address you entered has "
                       "already been registered.",), }
    email = models.EmailField(_('email address'), unique=True,
                              error_messages=msg, max_length=255, null=True,
                              blank=True)

    def __str__(self):
        return self.first_name


class RepairService(models.Model):
    """Defines a phone repair service."""
    repair_service = models.CharField(max_length=255)

    def __str__(self):
        return self.repair_service


class Service(models.Model):
    """
    Associates service people with phone services.
    """
    service = models.ForeignKey(RepairService, on_delete=models.SET_NULL,
                                null=True, blank=True)
    service_man = models.ForeignKey(ServicePerson, on_delete=models.SET_NULL,
                                    null=True, blank=True)

    class Meta:
        """
        Dictates that a service cannot be assigned the same service provider.
        twice.
        """
        unique_together = ('service', 'service_man')

    def __str__(self):
        return str(self.service)


class PhoneBrand(models.Model):
    """
    A table model to represent the brand of a phone. A phone brand in this
    case is a particular brand of phone for a particular company e.g Samsung
    that belongs to a particular Phone Category
    """
    brand_name_unique_message = _(
        "The brand name you entered already exists",)
    brand_name = models.CharField(
        max_length=255, unique=True, error_messages={
            'unique': brand_name_unique_message, },)
    brand_icon = models.CharField(max_length=60, blank=True, default='')

    def __str__(self):
        return self.brand_name


class PhoneModel(models.Model):
    """
    A table model to represent the model of a phone. A phone model in this
    case is an item within a particular category such as either an android
    phone, an iphone or a tablet. The item is of a particular brand lets
    say apple or samsung. But uniquely the item is of a particular brand
    model e.g. Samsung S7 This brand model then can have various phones
    within it that range based on color, price and size
    """
    class Meta:
        """Sets the plural name of PhoneModel."""
        verbose_name_plural = "PhoneModels"
    category = models.ForeignKey(PhoneCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    brand = models.ForeignKey(PhoneBrand, on_delete=models.SET_NULL,
                              null=True, blank=True)
    brand_model_unique_message = _(
        "The brand model you entered already exists",)
    brand_model = models.CharField(
        max_length=255, unique=True, error_messages={
            'unique': brand_model_unique_message, },)
    average_review = models.DecimalField(max_digits=2, decimal_places=1,
                                         default=5.0)
    brand_model_image = models.ImageField(upload_to="brand_models",
                                          default="brand_model_image_alt")

    def __str__(self):
        return self.brand_model


class PhoneModelList(models.Model):
    """
    A table model for phones within a particular Phone Model
    """
    phone_model = models.ForeignKey(PhoneModel, related_name='phone_list',
                                    on_delete=models.CASCADE)
    color = models.ForeignKey(
        Color, related_name='phone_color', on_delete=models.SET_NULL,
        null=True, blank=True)
    size_sku = models.ForeignKey(PhoneMemorySize, related_name='phone_size',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    quantity = IntegerRangeField(min_value=0)
    help_message = _('Designates whether this phone color is in stock. '
                     'Unselect this instead of deleting phone color.')
    is_in_stock = models.BooleanField(_('in_stock'), default=False,
                                      help_text=help_message, )
    main_image = models.ImageField(upload_to="phones")
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    def __str__(self):
        return "Phone Model: " + str(self.phone_model)

    @property
    def get_lowest_price(phone):
        """Returns the lowest price of a phone model."""
        return PhoneModelList.objects.filter(
            phone_model=phone.phone_model).order_by('price').first().price


class Cart(models.Model):
    """Creates carts for holding ordered items."""
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    quantity = IntegerRangeField(min_value=1)
    phone_model_item = models.ForeignKey(PhoneModelList,
                                         on_delete=models.CASCADE)
    session_key = models.CharField(
        _('session key'), max_length=40, null=True, blank=True)

    def __str__(self):
        if self.owner:
            return str(self.owner) + " date: " + str(self.creation_date)
        return "Anonymous User" + " date: " + str(self.creation_date)


class Order(models.Model):
    """
    A table model for order items.
    """
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    phone = models.ForeignKey(PhoneModelList, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    quantity = IntegerRangeField(min_value=1)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    size = models.CharField(max_length=4, null=True, blank=True)
    total_price = IntegerRangeField(min_value=0, default=0)
    payment_method = models.ForeignKey(PaymentMethod,
                                       on_delete=models.SET_NULL,
                                       blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True,
                             null=True)

    def __str__(self):
        return str(self.phone) + ": " + str(self.owner) + " date: " + \
            str(self.date)

    @property
    def get_address(order):
        return ShippingAddress.objects.filter(order=order).first()


class ShippingAddress(models.Model):
    """
    A table model for shipping addresses.
    """
    order = models.ForeignKey(Order, related_name='shipping_address',
                              on_delete=models.CASCADE)
    pickup = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    recepient = models.CharField(max_length=255, blank=True, null=True)


class Feature(models.Model):
    """
    A table model for phone features.
    """
    phone = models.ForeignKey(PhoneModelList, related_name='phone_features',
                              on_delete=models.CASCADE)
    feature = models.CharField(max_length=256)


class Review(models.Model):
    """
    A table model for phone reviews.
    """
    stars = IntegerRangeField(min_value=1, max_value=5)
    comments = models.TextField()
    phone_model = models.ForeignKey(PhoneModel, related_name='phone_reviews',
                                    on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateField(auto_now=True)

    def __str__(self):
        return (str(self.owner) + ": " + str(self.stars) + " stars: "
                + self.comments)


class ProductInformation(models.Model):
    """
    A table model for product information.
    """
    phone = models.ForeignKey(PhoneModelList, related_name='phone_information',
                              on_delete=models.CASCADE)
    feature = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


class PhoneImage(models.Model):
    """
    Creates Phone Images.
    """
    image = models.ImageField(upload_to="phones")
    images = models.ForeignKey(PhoneModelList, related_name='phone_images',
                               on_delete=models.SET_NULL, null=True,
                               blank=True)


class HotDeal(models.Model):
    """
    Creates HotDeal items.
    """
    item = models.ForeignKey(PhoneModelList, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item)

    def save(self, *args, **kwargs):
        """
        Overrides the default save behavior to update cache.
        """
        cache.delete('hot_deals')
        super(HotDeal, self).save(*args, **kwargs)


def delete_cache(model_class, object_id, cache_name):
    """
    Deletes HotDeal cache.
    """
    model_object = model_class.objects.get(pk=object_id)
    if model_object.category:
        cache.delete(cache_name.format(model_object.category.id))


@receiver(pre_delete, sender=PhoneCategory)
def clear_phone_categories_cache(sender, **kwargs):
    """Delete phone categories cache."""
    cache.delete('phone_categories')
    cache.delete("category_{}".format(kwargs["instance"].id))
    cache.delete("phones_{}".format(kwargs["instance"].id))
    cache.delete("sizes_{}".format(kwargs["instance"].id))


@receiver(pre_delete, sender=PhoneModelList)
def clear_phone_cache(sender, **kwargs):
    """Delete phones cache."""
    cache_delete("phones_{}", kwargs["instance"].category)


@receiver(pre_delete, sender=PhoneMemorySize)
def clear_phone_mem_size_cache(sender, **kwargs):
    """Delete phone memory sizes cache."""
    cache_delete("sizes_{}", kwargs["instance"].category)


@receiver(pre_delete, sender=SocialMedia)
def clear_social_media_cache(sender, **kwargs):
    """Delete social media cache."""
    cache.delete('social_media')


@receiver(pre_delete, sender=HotDeal)
def clear_hot_deals_cache(sender, **kwargs):
    """Clear HotDeals cache."""
    cache.delete('hot_deals')


@receiver(post_save, sender=Review)
def adjust_average_review(sender, **kwargs):
    average_review(kwargs["instance"].phone_model_id)


@receiver(post_delete, sender=Review)
def adjust_average_review_delete(sender, **kwargs):
    average_review(kwargs["instance"].phone_model_id)


def average_review(phone_model_id):
    """Calculate the average review of a phone."""
    reviews = Review.objects.filter(phone_model=phone_model_id)
    if reviews:
        counter = 0
        for review in reviews:
            counter += review.stars
        average = counter / reviews.count()
        phone_model = PhoneModel.objects.get(pk=phone_model_id)
        phone_model.average_review = average
        phone_model.save()
    else:
        phone_model = PhoneModelList.objects.get(pk=phone_model_id)
        phone_model.average_review = 5.0
        phone_model.save()


def cache_delete(cache_name, cache_id):
    """Delete application's cache."""
    if cache_id:
        cache.delete(cache_name.format(cache_id.id))
