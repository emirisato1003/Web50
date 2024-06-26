from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img']

class IconForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['icon_img']