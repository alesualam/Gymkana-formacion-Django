from django import forms

from .models import New

class PostForm(forms.ModelForm):

    class Meta:
        model = New
        field = ('title', 'subtitle', 'body', 'image')
        exclude = ('publish_date',)
