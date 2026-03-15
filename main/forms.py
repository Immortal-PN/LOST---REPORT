from django import forms
from .models import LostItem, FoundItem
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["username","email","password"]

        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
        }

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