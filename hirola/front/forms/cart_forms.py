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
        fields = ('phone_model_item', 'quantity', 'owner')

    def __init__(self, user, *args, **kwargs):
        self.user = user
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
