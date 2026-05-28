from django import forms
from .models import CustomUser, Package, PackageImage
from .models import PackagerProfile
from .models import CustomerProfile
from .models import Review
from .models import Booking
from.models import GalleryImage
from .models import FAQ
from .models import ChatMessage
from django.contrib.auth.forms import PasswordChangeForm


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    document = forms.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        user_type = cleaned_data.get("user_type")
        document = cleaned_data.get("document")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if user_type == 'packager' and not document:
            raise forms.ValidationError("Document is required for packagers.")
        

        if user_type == 'customer' and  document:
            raise forms.ValidationError("Document is not for customers.")

        return cleaned_data

    
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'description', 'long_description', 'short_description', 'price', 'main_image', 'map_url', 'phone_number', 'email']

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        if kwargs.get('instance') is None:  
            user_profile = kwargs['initial'].get('user').packager_profile if kwargs['initial'].get('user') else None
            if user_profile:
                self.fields['phone_number'].initial = user_profile.phone_number
                self.fields['email'].initial = user_profile.email


class PackageImageForm(forms.ModelForm):
    class Meta:
        model = PackageImage
        fields = ['image', 'description']


class PackagerProfileForm(forms.ModelForm):
    class Meta:
        model = PackagerProfile
        fields = ['name', 'location', 'profile_image', 'other_details', 'phone_number', 'email', 'map_url']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['name', 'profile_image', 'location', 'other_details']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Write your review here...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class BookingForm(forms.ModelForm):
    travel_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['travel_date', 'num_travelers', 'phone_number', 'email', 'address', 'additional_info']


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question'] 


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=19, required=True) 
    expiry_month = forms.CharField(max_length=2, required=True)
    expiry_year = forms.CharField(max_length=4, required=True)
    cvc = forms.CharField(max_length=4, required=True)
  

class ChatForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))

    class Meta:
        model = ChatMessage
        fields = ['message']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
        label='Current Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label='Confirm New Password'
    )
