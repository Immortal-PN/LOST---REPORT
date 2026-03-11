from django import forms
from .models import LostItem, FoundItem


class LostItemForm(forms.ModelForm):

    class Meta:
        model = LostItem
        fields = '__all__'

    def clean_image(self):

        image = self.cleaned_data.get('image')

        if image:

            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image must be under 2MB")

        return image


class FoundItemForm(forms.ModelForm):

    class Meta:
        model = FoundItem
        fields = '__all__'

    def clean_image(self):

        image = self.cleaned_data.get('image')

        if image:

            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image must be under 2MB")

        return image