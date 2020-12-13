from django import forms
from django.core import validators


class FormInput(forms.Form):
    Input = forms.CharField(widget=forms.Textarea, label='')
    botCatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
