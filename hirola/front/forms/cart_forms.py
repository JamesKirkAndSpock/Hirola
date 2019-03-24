from front.forms.base_form import forms
from front.models import Cart


class CartForm(forms.ModelForm):
    """
    A form to collect user data on phone profile page.
    """

    class Meta:
        """
        This class attaches the model and fields to the UserCreationForm
        """
        model = Cart
        fields = ('phone_model_item', 'quantity', 'owner', 'session_key',
                  'is_wishlist')

    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_owner(self):
        owner = self.cleaned_data['owner']
        if not self.user.is_anonymous:
            return self.user
        return owner

    def clean_session_key(self):
        session_key = self.cleaned_data['session_key']
        if self.user.is_anonymous and not self.instance.pk:
            session_key = self.request.session.session_key
        return session_key

    def clean_is_wishlist(self):
        is_wishlist = self.cleaned_data['is_wishlist']
        return is_wishlist
