from django import forms

from django.core.exceptions import ValidationError

from .models import New


class PostForm(forms.ModelForm):

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 10 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 10mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

    class Meta:
        model = New
        field = ('title', 'subtitle', 'body', 'image')
        exclude = ('publish_date',)
