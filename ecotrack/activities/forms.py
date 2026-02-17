from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["date", "category", "quantity", "unit", "description"]

        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "e.g., 10",
                }
            ),
            "unit": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., km, kg, kWh"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional details...",
                }
            ),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            validation_err_message = "The activity date cannot be in the future."
            raise ValidationError(validation_err_message)
        return date
