from django import forms
from django.forms import DateTimeField

from django.core.exceptions import ValidationError

from .models import New, Event

from django.conf import settings


class PostForm(forms.ModelForm):

    class Meta:
        model = New
        field = ('title', 'subtitle', 'body', 'image')
        exclude = ('publish_date',)

    def clean_image(self):

        image = self.cleaned_data.get('image', False)
        if image == settings.IMAGE_DEFAULT:
            return image
        else:
            if image.size > 10 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 10mb )")
            else:
                return image

class EventForm(forms.ModelForm):

    start_date = DateTimeField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=["%d/%m/%Y"])
    end_date = DateTimeField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=["%d/%m/%Y"])

    class Meta:
        model = Event
        field = ('title', 'subtitle', 'body', 'start_date', 'end_date')
        exclude = ()

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date', False)
        end_date = self.cleaned_data.get('end_date', False)

        if start_date > end_date:
            raise ValidationError("Ending date must be set after Starting date")
        else:
            return end_date
