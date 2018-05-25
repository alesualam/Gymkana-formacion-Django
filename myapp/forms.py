from django import forms

from django.core.exceptions import ValidationError

from .models import New

from django.conf import settings


class PostForm(forms.ModelForm):

    class Meta:
        model = New
        field = ('title', 'subtitle', 'body', 'image')
        exclude = ('publish_date',)

    def clean_image(self):
        import ipdb;ipdb.set_trace()
        image = self.cleaned_data.get('image', False)
        if image == settings.IMAGE_DEFAULT:
            return image
        else:
            if image.size > 10 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 10mb )")
            else:
                return image
