from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "instructor", "price", "category", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Asynchronous Microservices with Python",
                "required": True,
            }),
            "instructor": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Alex Rivera",
                "required": True,
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-input",
                "step": "0.01",
                "required": True,
            }),
            "category": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Backend, AI, Database",
                "required": True,
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "checkbox-input",
            }),
        }

    def clean_price(self) -> float:
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Course price cannot be negative.")
        return price
