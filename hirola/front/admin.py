"""Contains models for the admin interface."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    PhoneImage, Review, Feature,
    ProductInformation, ShippingAddress,
    PhoneMemorySize, Currency, SocialMedia, Order,
    OrderStatus, ItemIcon, NewsItem, InactiveUser, Color,
    Cart, RepairService, Address, ServicePerson, Service,
    PhoneBrand, PhoneModel, PhoneModelList, CancelledOrder
    )
from .forms.model_forms import (
    PhoneCategoryForm, HotDealForm,
    PhoneCategory, HotDeal, ServicePersonForm
    )
from .forms.user_forms import (
    UserChangeForm, UserCreationForm,
    User, CountryCode
    )


class PhoneCategoryAdmin(admin.ModelAdmin):
    """Represents the PhoneCategory model"""
    form = PhoneCategoryForm


class PhoneImageInline(admin.TabularInline):
    """Represents the PhoneImage model."""
    model = PhoneImage
    extra = 3


class PhoneReviewInline(admin.TabularInline):
    """Represents the Review model."""
    model = Review
    extra = 1


class PhoneFeatureInline(admin.TabularInline):
    """Represents the Feature model."""
    model = Feature
    extra = 1


class PhoneProductInline(admin.StackedInline):
    """Represents the ProductInformation model."""
    model = ProductInformation
    extra = 1


class OrderInline(admin.StackedInline):
    """
    Order inline form
    """
    model = Order
    extra = 1
    max_num = 1


class ShippingAddressAdmin(admin.ModelAdmin):
    inlines = [OrderInline]


class PhoneModelListInline(admin.StackedInline):
    """Represents the PhoneModelList model."""
    model = PhoneModelList
    extra = 0


class PhoneModelAdmin(admin.ModelAdmin):
    """
    Implements inline layout for PhoneModelListInline,
    PhoneReviewInline.
    """
    inlines = [PhoneModelListInline, PhoneReviewInline]


class PhoneModelInline(admin.TabularInline):
    """Represents the PhoneModel model."""
    model = PhoneModel
    extra = 0


class PhoneModelListAdmin(admin.ModelAdmin):
    """
    Represents the PhoneModelList model.
    """
    inlines = [PhoneFeatureInline, PhoneProductInline, PhoneImageInline]
    model = PhoneModelList
    extra = 0


class PhoneBrandAdmin(admin.ModelAdmin):
    """
    Implements an inline layout for PhoneModelInline on the admin interface.
    """
    inlines = [PhoneModelInline]


class UserAdmin(BaseUserAdmin):
    """
    Represents the admin user profile page.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'country_code', 'phone_number',
                                         'photo',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


class HotDealAdmin(admin.ModelAdmin):
    """Represents the HotDeal model data collection form."""
    form = HotDealForm


class ServicePersonAdmin(admin.ModelAdmin):
    """Represents the ServicePersonForm model data collection form."""
    form = ServicePersonForm


admin.site.register(PhoneCategory, PhoneCategoryAdmin)
admin.site.register(PhoneMemorySize)
admin.site.register(Currency)
admin.site.register(SocialMedia)
admin.site.register(User, UserAdmin)
admin.site.register(CountryCode)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(HotDeal, HotDealAdmin)
admin.site.register(ItemIcon)
admin.site.register(NewsItem)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(InactiveUser)
admin.site.register(Color)
admin.site.register(Cart)
admin.site.register(RepairService)
admin.site.register(Address)
admin.site.register(ServicePerson, ServicePersonAdmin)
admin.site.register(Service)
admin.site.register(PhoneBrand, PhoneBrandAdmin)
admin.site.register(PhoneModel, PhoneModelAdmin)
admin.site.register(PhoneModelList, PhoneModelListAdmin)
admin.site.register(CancelledOrder)
