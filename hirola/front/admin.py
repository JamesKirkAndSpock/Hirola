from django.contrib import admin
from .models import *
from .forms import *


class LandingPageImageAdmin(admin.ModelAdmin):
    form = LandingPageImageForm


class PhoneCategoryListAdmin(admin.ModelAdmin):
    form = PhoneCategoryListForm


class PhoneListAdmin(admin.ModelAdmin):
    form = PhoneListForm
    change_form_template = 'admin/front/phone_list.html'

admin.site.register(LandingPageImage, LandingPageImageAdmin)
admin.site.register(PhoneCategoryList, PhoneCategoryListAdmin)
admin.site.register(PhoneList, PhoneListAdmin)
admin.site.register(PhoneMemorySize)
admin.site.register(Currency)
admin.site.register(SocialMedia)
