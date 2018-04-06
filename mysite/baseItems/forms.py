from django import forms
from .models import Event, New
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'subtitle', 'body', 'image']
        # fields = '__all__'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if isinstance(image, InMemoryUploadedFile) or isinstance(image, TemporaryUploadedFile):
            image_name = image.name
            image_split = image_name.split('.')
            image_format = image_split[-1]
            formats = ['jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG']
            if image_format not in formats:
                raise forms.ValidationError("Wrong format, only jpg, jpeg, png")
            elif image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Too heavy image, less than 10 MB please")
            else:
                return image


class EventsForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {'start_date': forms.widgets.SelectDateWidget(years=range(2000, 2020)), 'end_date': forms.widgets.SelectDateWidget(years=range(2000, 2025))}

    def clean(self):
        cleaned_data = super(EventsForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("End date can't be before than start date")


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
