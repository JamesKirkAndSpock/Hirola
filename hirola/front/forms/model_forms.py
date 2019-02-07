from .base_form import *
from django.core.files.images import get_image_dimensions
from front.models import PhoneCategory, HotDeal, PhonesColor


class PhoneCategoryForm(forms.ModelForm):

    def clean(self):
        data = self.cleaned_data
        category = self.cleaned_data["phone_category"]
        if PhoneCategory.objects.count() >= 4 and self.instance.pk is None:
            raise ValidationError(phone_category_error)
        if PhoneCategory.objects.filter(phone_category=category) and not self.instance.pk:
            error_message = phone_category_error_2.format(category)
            raise ValidationError(error_message)
        return data

    def clean_category_image(self):
        data = self.cleaned_data['category_image']
        width, height = get_image_dimensions(data)
        if height != width:
            raise ValidationError(category_image_error.format(height, width))
        return data


class HotDealForm(forms.ModelForm):

    def clean(self):
        data = self.cleaned_data
        item = self.cleaned_data["item"]
        if HotDeal.objects.filter(item=item) and not self.instance.pk:
            error_message = hot_deal_error.format(item)
            raise ValidationError(error_message)
        return data
