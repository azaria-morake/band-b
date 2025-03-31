from django import forms
from .models import House, Amenity, HouseImage, UserProfile

class HouseForm(forms.ModelForm):
    amenities_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Amenities",
        help_text="Enter amenities separated by commas (e.g., WiFi, Parking, Pool)"
    )
    
    class Meta:
        model = House
        fields = ['title', 'description', 'price', 'address', 'amenities_text']
        labels = {
            'title': 'Property Name',
            'price': 'Nightly Price ($)',
            'address': 'Full Property Address'
        }

class HouseImageForm(forms.ModelForm):
    class Meta:
        model = HouseImage
        fields = ['image']
class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return super().save(commit)