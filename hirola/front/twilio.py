from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from django import forms
from django.utils.translation import gettext_lazy as _


class TwilioValidation():
    error_messages = {
        'invalid_number': _("The phone number entered is invalid."),
        'unknown_error': _("There was an error validating your number."),
    }

    def phone_validation(self, country_code, phone_number):
        phone_check = str(country_code.country_code) + str(phone_number)
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
