from django import forms
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from .models import PhoneCategoryList
from .errors import *


class LandingPageImageForm(forms.ModelForm):

    def clean_photo(self):
        data = self.cleaned_data['photo']
        w, h = get_image_dimensions(data)

        if w < 1280 and h < 700:
            raise ValidationError(landing_page_error.format(w, h))
        return data


class PhoneCategoryListForm(forms.ModelForm):

    def clean(self):
        data = self.cleaned_data
        category = self.cleaned_data["phone_category"]
        if PhoneCategoryList.objects.count() >= 4 and self.instance.pk is None:
            raise ValidationError(phone_category_error)
        if PhoneCategoryList.objects.filter(phone_category=category):
            error_message = phone_category_error_2.format(category)
            raise ValidationError(error_message)
        return data


class PhoneListForm(forms.ModelForm):

    def clean_phone_image(self):
        data = self.cleaned_data['phone_image']
        w, h = get_image_dimensions(data)
        if h > 150 or h < 150 or w > 81 or w < 70:
            raise ValidationError(phone_list_error.format(w, h))
        return data
