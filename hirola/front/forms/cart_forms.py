from front.forms.base_form import forms
from front.models import Cart, CartOwner, ShippingAddress
from front.twilio import TwilioValidation


class CartForm(forms.ModelForm):
    """
    A form to collect user data on phone profile page.
    """

    class Meta:
        """
        This class attaches the model and fields to the UserCreationForm
        """
        model = Cart
        fields = ('phone_model_item', 'quantity', 'owner',
                  'session_key', 'is_wishlist')

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

    def clean_phone_size_sku(self):
        if self.cleaned_data['phone_size_sku']:
            phone_size_sku = self.cleaned_data['phone_size_sku']
            return int(phone_size_sku)


class CartOwnerForm(forms.ModelForm):
    """
    A form to collect temporary cart and owner information
    """

    class Meta:
        """
        This class attaches the model and fields to the CartOwnerForm
        """
        model = CartOwner
        fields = ('cart', 'owner')

    def clean(self):
        data = self.cleaned_data
        cart = self.cleaned_data['cart']
        owner = self.cleaned_data['owner']
        existent_cart = CartOwner.objects.filter(
            cart=cart, owner=owner).first()
        if existent_cart:
            self.add_error(None, "Relation already exists")
            return None
        return data


class ShippingAddressForm(forms.ModelForm):
    """
    Collects order details
    """

    class Meta:
        """
        Attaches the ShippingAddress model to the form fields.
        """

        model = ShippingAddress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields['hidden_pickup'] = forms.CharField(
            widget=forms.TextInput(
                attrs={'required': False, 'id': 'pickupOption'}))

    def clean_phone_number(self):
        """
        Validate phone number.
        """
        country_code = self.cleaned_data.get("country_code")
        if not country_code:
            raise forms.ValidationError("Enter a valid country code")
        phone_number = self.cleaned_data.get("phone_number")
        return TwilioValidation().phone_validation(country_code, phone_number)

    def save(self, commit=True):
        """
        Save address to the database.
        """
        address = super().save(commit=False)
        address.pickup = False
        if commit:
            address.save()
        return address
