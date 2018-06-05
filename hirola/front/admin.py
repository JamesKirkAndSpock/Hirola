from django.contrib import admin
from django import forms
from .models import LandingPageImage
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.contrib import messages


class LandingPageImageForm(forms.ModelForm):
    def clean_photo(self):
        data = self.cleaned_data['photo']
        w, h = get_image_dimensions(data)
        if w < 1280 and h <700:
            error_message="The dimensions of your image are "
            error_message+=str(w) +" pixels (width) by " + str(h) + " pixels (height)."
            error_message+="\nThe landing page has to have a width of "
            error_message+="1280 pixels or more and a height of 700 pixels or "
            error_message+="more for clear images"
            raise ValidationError(error_message)
        return data
        
    
class LandingPageImageAdmin(admin.ModelAdmin):
    form = LandingPageImageForm

admin.site.register(LandingPageImage, LandingPageImageAdmin)
