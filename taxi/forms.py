import re
from django import forms
from django.contrib.auth import get_user_model

from .models import Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        value = self.cleaned_data["license_number"].strip().upper()
        license_re = re.compile(r"^[A-Z]{3}\d{5}$")
        if not license_re.fullmatch(value):
            raise forms.ValidationError(
                "The license number must be 8 characters long: "
                "3 uppercase Latin letters followed by 5 digits "
                "(e.g., ABC12345)."
            )
        return value


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
