from .base_form import *
from django.core.files.images import get_image_dimensions
from front.models import PhoneCategoryList


class LandingPageImageForm(forms.ModelForm):

    def clean_photo(self):
        data = self.cleaned_data['photo']
        width, height = get_image_dimensions(data)

        if width < 1280 and height < 700:
            raise ValidationError(landing_page_error.format(width, height))
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
        width, height = get_image_dimensions(data)
        if height > 150 or height < 150 or width > 81 or width < 70:
            raise ValidationError(phone_list_error.format(width, height))
        return data