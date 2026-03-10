from django import forms
from .models import LostItem, FoundItem


class LostItemForm(forms.ModelForm):

    class Meta:
        model = LostItem
        fields = '__all__'


class FoundItemForm(forms.ModelForm):

    class Meta:
        model = FoundItem
        fields = '__all__'