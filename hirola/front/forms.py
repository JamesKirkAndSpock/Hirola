'''
Forms
'''
from django import forms
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .models import PhoneCategoryList
from .errors import *
from .models import User


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


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges from the given email and
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'invalid_number': _("The phone number entered is invalid."),
        'unknown_error': _("There was an error validating your number."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'area_code',
                  'phone_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_phone_number(self):
        area_code = self.cleaned_data.get("area_code")
        phone_number = self.cleaned_data.get("phone_number")
        if area_code and phone_number:
            phone_check = str(area_code.area_code) + str(phone_number)
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            try:
                client.lookups.phone_numbers("+" + phone_check).fetch()
                return phone_number
            except TwilioRestException as etwilio:
                if etwilio.code == 20404:
                    raise forms.ValidationError(
                        self.error_messages['invalid_number'],
                        code='invalid_number',
                    )
                else:
                    raise forms.ValidationError(
                        self.error_messages['unknown error'],
                        code='unknown error',
                    )

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the passowrd using "
            "<a href=\"{}\">this form</a>."
        )
    )

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users.
    """
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    email = forms.EmailField(
        label=_('Email address'),
        max_length=255)

    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standarad 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email,
                                           password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.
        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )
