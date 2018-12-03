from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
from .forms.model_forms import *
from .forms.user_forms import *


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


class PhoneProductInline(admin.StackedInline):
    model = ProductInformation
    extra = 1


class PhoneListAdmin(admin.ModelAdmin):
    inlines = [PhoneImageInline, PhoneReviewInline, PhoneFeatureInline, PhoneProductInline, ]
    change_form_template = 'admin/front/phone_list.html'


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'area_code', 'phone_number')}),
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

admin.site.register(PhoneCategory, PhoneCategoryAdmin)
admin.site.register(PhoneList, PhoneListAdmin)
admin.site.register(PhoneMemorySize)
admin.site.register(Currency)
admin.site.register(SocialMedia)
admin.site.register(User, UserAdmin)
admin.site.register(AreaCode)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(HotDeal, HotDealAdmin)
admin.site.register(ItemIcon)
