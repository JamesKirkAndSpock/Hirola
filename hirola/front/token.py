"""Contains functionality to generate various tokens."""
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generates a toke for reseting password
    """
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )


class ChangeEmailTokenGenerator(PasswordResetTokenGenerator):
    """
    Generates token for changing email.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_change_allowed)
            + str(user.change_email)
        )


account_activation_token = TokenGenerator()
email_activation_token = ChangeEmailTokenGenerator()
