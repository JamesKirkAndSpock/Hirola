"""This module contains forms for collecting data from the user."""
import re
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.validators import validate_email
from django.conf import settings
from front.models import CountryCode, User
from front.token import account_activation_token, email_activation_token
from front.twilio import TwilioValidation
from front.forms.base_form import (forms, ValidationError)


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
        """
        This class attaches the model and fields to the UserCreationForm
        """
        model = User
        fields = ('email', 'first_name', 'last_name', 'country_code',
                  'phone_number')

    def clean_password2(self):
        """
        Validate that both passwords entered by the user match.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def send_email(self, request, user):
        """
        Send email to user after successful registration.

        parameters:
            request(object): Contains metadata about the request
            user(object): Object representing the user requesting for
            registration
        """
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        to_email = self.cleaned_data.get('email')
        subject = loader.render_to_string(
            "registration/signup_activation_subject.txt", context
            )
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(
            "registration/signup_activation_email.html", context
            )
        email_message = EmailMultiAlternatives(subject, body, None, [to_email])
        email_message.send()

    def get_user(self, uidb64):
        """
        Return a user object based on the user's id encoded in base 64.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def clean_phone_number(self):
        """
        Validate the phone number provided by the user.
        """
        country_code = self.cleaned_data.get("country_code")
        phone_number = self.cleaned_data.get("phone_number")
        return TwilioValidation().phone_validation(country_code, phone_number)

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        """
        Save user to the database.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form form to enable a user to edit their profile information."""
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the passowrd using "
            "<a href=\"{}\">this form</a>."
        )
    )

    class Meta:
        """Contains metadata for the ModelForm class"""
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.\
                select_related('content_type')

    def clean_password(self):
        """
        Get the set initial value of password.
        """
        return self.initial["password"]


class UserForm(forms.ModelForm):
    """A form to collect user registration data."""
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the passowrd using "
            "<a href=\"{}\">this form</a>."
        )
    )

    class Meta:
        """Contains metadata for the ModelForm class"""
        model = User
        fields = (
            'first_name', 'last_name', 'country_code', 'phone_number',
            'password'
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country_code"].required = False

    def save(self, commit=True):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """
        self.instance = self.fill_fields()
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance

    def fill_fields(self):
        """Set the inital values of the fields."""
        initial_fields = self.fields.keys() - self.data.keys()
        for field in initial_fields:
            if field == "country_code":
                setattr(self.instance, field,
                        CountryCode.objects.get(pk=self.initial[field]))
            else:
                setattr(self.instance, field, self.initial[field])
        return self.instance

    def clean_phone_number(self):
        """
        Validate phone number entered by the user.
        """
        country_code = CountryCode.objects.get(pk=self.initial["country_code"])
        phone_number = self.initial["phone_number"]
        return TwilioValidation().phone_validation(country_code, phone_number)


class OldPasswordForm(forms.Form):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly."
                                " Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    field_order = ['old_password']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


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
        'invalid_email': _(
            "You entered an incorrect email!!!"
        ),
        'non_existent': _(
            "We cannot find an account with that email address."
            ),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.redirect = False

    def clean(self):
        """
        Get user data, authenticate and set cache.
        """
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

    def clean_email(self):
        """Validate email is correct."""
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError(
                self.error_messages['non_existent'],
                code='non_existent',
            )
        self.confirm_login_allowed(user)
        return email

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
            self.redirect = True
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        """
        Get logged in user from cache.

        Returns:
            user(object): authenticated user
        """
        return self.user_cache

    def get_invalid_login_error(self):
        """
        Raise invalid login error.

        Returns:
            error(object): Contains a message of what went wrong.
        """
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )


class ChangeEmailForm(forms.ModelForm):
    """
    A form that lets a user change their email
    """

    error_messages = {
        'invalid_email': _(
            "The email you have entered looks similar to your former email!"
        ),
    }

    class Meta:
        """Contains metadata for the ChangeEmailForm class"""
        model = User
        fields = ('email',)

    def send_email(self, request, user):
        """Send email."""
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': email_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        to_email = self.cleaned_data.get('email')
        subject = loader.render_to_string(
            "front/change_email_activation_subject.txt", context
            )
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(
            "front/change_email_activation_email.html", context
            )
        email_message = EmailMultiAlternatives(subject, body, None, [to_email])
        email_message.send()

    def clean_email(self):
        """
        Validate email is correct.

        Returns:
            email(str): Returns user email if valid

        Raises:
            ValidationError(object): Invalid email exception
        """
        email = self.cleaned_data.get("email")
        if self.initial["email"] == email:
            raise forms.ValidationError(
                self.error_messages['invalid_email'],
                code='invalid_email',
            )
        return email


class EmailAuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users.
    """

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.request.user.email:
            raise forms.ValidationError(
                self.error_messages['invalid_email'],
                code='invalid_email',
            )
        return email


def validate_user_email(email):
    """
    Validate email.

    parameters:
        email(str): email to validate
    """
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True


def resend_email(request, user, email):
    """
    Resend user email.

    parameters:
        request(object): Passes state between views.
        user(object): User engaging the site
        email(str): User email to resend the email to
    """
    if validate_user_email(email):
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        to_email = email
        subject = loader.render_to_string(
            "registration/signup_activation_subject.txt", context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(
            "registration/signup_activation_email.html", context)
        email_message = EmailMultiAlternatives(subject, body, None, [to_email])
        email_message.send()
        return True
    return False


def resend_activation_email(request, user, email):
    """Resend link to activate email."""
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': email_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    to_email = email
    subject = loader.render_to_string(
        "front/change_email_activation_subject.txt", context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(
        "front/change_email_activation_email.html", context)
    email_message = EmailMultiAlternatives(subject, body, None, [to_email])
    email_message.send()
    return True


class ContactUsForm(forms.Form):
    """
    Form to collect user data in the contact page.
    """
    error_messages = {
        'invalid': _('Please enter a valid comment'),
        'required': _("Comment cannot be empty!")
    }

    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Name(Optional)'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Tell us about the issue..',
               'class': 'materialize-textarea'}))

    def clean_comment(self):
        """Validate comment."""
        comment = self.cleaned_data.get('comment')
        if not comment or comment.isspace():
            raise ValidationError(self.error_messages['required'])
        if re.match(r'^[_\W]+$', comment):
            raise ValidationError(self.error_messages['invalid'])
        return comment

    def send_email(self):
        """Send email to site administrators."""
        to_email = settings.EMAIL_HOST_USER
        from_email = settings.DEFAULT_FROM_EMAIL
        sender_name = self.cleaned_data.get('name') or 'Anonymous User'
        email = self.cleaned_data.get('email')
        subject = "Help and support request from {} of email {}".format(
            sender_name, email
        )
        body = self.cleaned_data.get('comment')
        body += '\n'
        body += from_email
        if subject and body and from_email:
            email_message = EmailMultiAlternatives(
                subject, body, from_email, [to_email]
            )
            email_message.send()


class OrderCancellationForm(forms.Form):
    """
    Form to collect user reason to collect data.
    """
    error_messages = {
        'invalid': _('Please enter a valid reason')
    }

    other_reason = forms.CharField(required=False)
    hidden = forms.CharField(required=False)

    def clean_other_reason(self):
        """Validate 'other' reason."""
        reason = self.cleaned_data.get('other_reason')
        if re.match(r'^[_\W]+$', reason) or reason.isspace():
            raise ValidationError(self.error_messages['invalid'])
        return reason

    def clean_hidden(self):
        """Validate radio choices reason."""
        hidden_reason = self.cleaned_data.get('hidden')
        return hidden_reason

    def send_email(self, request):
        """Send email to site administrators."""
        to_email = settings.EMAIL_HOST_USER
        email = request.user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = "Reason for Cancelling Order"
        body = ""
        if self.clean_hidden():
            body = self.clean_hidden()
        else:
            body = self.clean_other_reason()
        body += '\n'
        body += 'From ' + email
        if subject and body and email:
            email_message = EmailMultiAlternatives(
                subject, body, from_email, [to_email]
            )
            email_message.send()
