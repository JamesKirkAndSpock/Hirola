from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (PhoneImage, Review, Feature, PhonesColor,
                     ProductInformation, ShippingAddress, PhoneList,
                     PhoneMemorySize, Currency, SocialMedia, Order,
                     OrderStatus, ItemIcon, NewsItem, InactiveUser, Color,
                     Cart, RepairService, Address, ServicePerson, Service,
                     PhoneBrand, PhoneModel, PhoneModelList)
from .forms.model_forms import (PhoneCategoryForm, HotDealForm,
                                PhoneCategory, HotDeal, ServicePersonForm)
from .forms.user_forms import (UserChangeForm, UserCreationForm,
                               User, CountryCode)


class PhoneCategoryAdmin(admin.ModelAdmin):
    form = PhoneCategoryForm


class PhoneImageInline(admin.TabularInline):
    model = PhoneImage
    extra = 3


class PhoneReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class PhoneFeatureInline(admin.TabularInline):
    model = Feature
    extra = 1


class PhoneColorInline(admin.TabularInline):
    model = PhonesColor
    extra = 1


class PhoneProductInline(admin.StackedInline):
    model = ProductInformation
    extra = 1


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 1
    max_num = 1


class PhoneModelListInline(admin.StackedInline):
    model = PhoneModelList
    extra = 0


class PhoneModelAdmin(admin.ModelAdmin):
    inlines = [PhoneModelListInline, PhoneReviewInline]


class PhoneModelInline(admin.TabularInline):
    model = PhoneModel
    extra = 0


class PhoneModelListAdmin(admin.ModelAdmin):
    inlines = [PhoneFeatureInline, PhoneProductInline, PhoneImageInline]
    model = PhoneModelList
    extra = 0


class PhoneBrandAdmin(admin.ModelAdmin):
    inlines = [PhoneModelInline]


class OrderAdmin(admin.ModelAdmin):
    inlines = [ShippingAddressInline, ]


class UserAdmin(BaseUserAdmin):
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
    form = HotDealForm


class ServicePersonAdmin(admin.ModelAdmin):
    form = ServicePersonForm


admin.site.register(PhoneCategory, PhoneCategoryAdmin)
admin.site.register(PhoneMemorySize)
admin.site.register(Currency)
admin.site.register(SocialMedia)
admin.site.register(User, UserAdmin)
admin.site.register(CountryCode)
admin.site.register(OrderStatus)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
admin.site.register(HotDeal, HotDealAdmin)
admin.site.register(ItemIcon)
admin.site.register(NewsItem)
admin.site.register(ShippingAddress)
admin.site.register(InactiveUser)
admin.site.register(Color)
admin.site.register(PhonesColor)
admin.site.register(Cart)
admin.site.register(RepairService)
admin.site.register(Address)
admin.site.register(ServicePerson, ServicePersonAdmin)
admin.site.register(Service)
admin.site.register(PhoneBrand, PhoneBrandAdmin)
admin.site.register(PhoneModel, PhoneModelAdmin)
admin.site.register(PhoneModelList, PhoneModelListAdmin)
admin.site.register(PhoneList)
