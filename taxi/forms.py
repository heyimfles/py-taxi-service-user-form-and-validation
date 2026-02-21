from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidationMixin(object):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Incorrect license number value")

        for char in license_number[:3]:
            if not char.isalpha() and not char.isupper():
                raise ValidationError("Incorrect license number value")

        for char in license_number[3:]:
            if not char.isdigit():
                raise ValidationError("Incorrect license number value")

        return license_number


class DriverCreationForm(
    UserCreationForm,
    LicenseNumberValidationMixin
):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(
    UserChangeForm,
    LicenseNumberValidationMixin
):

    class Meta:
        model = Driver
        fields = ("license_number",)
        exclude = ("password",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
