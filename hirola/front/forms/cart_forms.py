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
        fields = ('phone_model_item', 'quantity', 'owner', 'session_key')

    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_owner(self):
        owner = self.cleaned_data['owner']
        if not self.user.is_anonymous:
            return self.user
        return owner

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.instance.pk:
            quantity = self.instance.quantity + self.cleaned_data['quantity']
        return quantity

    def clean_session_key(self):
        session_key = self.cleaned_data['session_key']
        if self.user.is_anonymous and not self.instance.pk:
            session_key = self.request.session.session_key
        return session_key
