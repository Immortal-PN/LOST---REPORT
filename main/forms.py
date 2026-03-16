from .models import LostItem, FoundItem
from django import forms

class LostItemForm(forms.ModelForm):

    class Meta:
        model = LostItem

        fields = [
            "title",
            "description",
            "category",
            "location",
            "date_lost",
            "image",
            "proof_document",
        ]

        widgets = {

            "title": forms.TextInput(attrs={"class":"form-control"}),

            "description": forms.Textarea(attrs={"class":"form-control"}),

            "category": forms.Select(attrs={"class":"form-control"}),

            "location": forms.TextInput(attrs={"class":"form-control"}),

            "date_lost": forms.DateInput(
                attrs={"class":"form-control","type":"date"}
            ),

        }


class FoundItemForm(forms.ModelForm):

    class Meta:
        model = FoundItem

        fields = [
            "title",
            "description",
            "category",
            "location",
            "date_found",
            "image",
        ]

        widgets = {

            "title": forms.TextInput(attrs={"class":"form-control"}),

            "description": forms.Textarea(attrs={"class":"form-control"}),

            "category": forms.Select(attrs={"class":"form-control"}),

            "location": forms.TextInput(attrs={"class":"form-control"}),

            "date_found": forms.DateInput(
                attrs={"class":"form-control","type":"date"}
            ),

        }
