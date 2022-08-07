from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'nickname',
            #'auto_key',
        )
        widgets = {
            'nickname': forms.TextInput,
        }