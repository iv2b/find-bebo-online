from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm

from tweb.models import CustomUser


class UserCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "user-crispy-form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "avatar")


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # fields = UserCreationForm.Meta.fields + ('avatar',)
        fields = UserCreationForm.Meta.fields
