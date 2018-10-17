from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
from .forms.model_forms import *
from .forms.user_forms import *


class LandingPageImageAdmin(admin.ModelAdmin):
    form = LandingPageImageForm


class PhoneCategoryListAdmin(admin.ModelAdmin):
    form = PhoneCategoryListForm


class PhoneListAdmin(admin.ModelAdmin):
    form = PhoneListForm
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


admin.site.register(LandingPageImage, LandingPageImageAdmin)
admin.site.register(PhoneCategoryList, PhoneCategoryListAdmin)
admin.site.register(PhoneList, PhoneListAdmin)
admin.site.register(PhoneMemorySize)
admin.site.register(Currency)
admin.site.register(SocialMedia)
admin.site.register(User, UserAdmin)
admin.site.register(AreaCode)
admin.site.register(OrderStatus)
admin.site.register(Orders)
admin.site.register(Reviews)
