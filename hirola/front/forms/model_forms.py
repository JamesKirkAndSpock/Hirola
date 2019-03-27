"""This module contains forms for collecting data from the admin."""
from django.core.files.images import get_image_dimensions
from front.twilio import TwilioValidation
from front.models import PhoneCategory, HotDeal
from .base_form import (
    ValidationError, forms, phone_category_error,
    category_image_error, phone_category_error_2,
    hot_deal_error
    )


class PhoneCategoryForm(forms.ModelForm):
    """A form for validating Phone category data."""

    def clean(self):
        """
        Validate that categories do not exceed four and a category has not
        been repeated.
        """
        data = self.cleaned_data
        category = self.cleaned_data["phone_category"]
        if PhoneCategory.objects.count() >= 4 and self.instance.pk is None:
            raise ValidationError(phone_category_error)
        if PhoneCategory.objects.filter(phone_category=category) and\
                not self.instance.pk:
            error_message = phone_category_error_2.format(category)
            raise ValidationError(error_message)
        return data

    def clean_category_image(self):
        """Validate that the height and width of the image are equal."""
        data = self.cleaned_data['category_image']
        width, height = get_image_dimensions(data)
        if height != width:
            raise ValidationError(category_image_error.format(height, width))
        return data


class HotDealForm(forms.ModelForm):
    """A form for validating HotDeal data."""

    def clean(self):
        """
        Validate that a hotdeal for a particular phone is only created once.
        """
        data = self.cleaned_data
        item = self.cleaned_data["item"]
        if HotDeal.objects.filter(item=item) and not self.instance.pk:
            error_message = hot_deal_error.format(item)
            raise ValidationError(error_message)
        return data


class ServicePersonForm(forms.ModelForm):
    """A form for checking ServicePerson data."""

    def clean_phone_number(self):
        """Validate phone number."""
        country_code = self.cleaned_data.get("country_code")
        phone_number = self.cleaned_data.get("phone_number")
        if not country_code:
            raise forms.ValidationError("Enter a valid country code")
        return TwilioValidation().phone_validation(country_code, phone_number)
