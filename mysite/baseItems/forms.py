from django import forms

from .models import New


class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'subtitle', 'body', 'image']


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
