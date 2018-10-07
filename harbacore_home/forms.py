from django import forms
from django.core import validators

#custom validator
def must_be_empty(value):
    if value:
        raise forms.ValidationError("is not empty ")

class ContactForm(forms.Form):
    name = forms.CharField(initial="What's your name")
    email = forms.EmailField(initial="Help us with your email")
    contact_no = forms.IntegerField(required=False , initial="1234567890")
    message = forms.CharField(widget=forms.Textarea, initial="Let me help you out")
    honeypot_for_bot_check = forms.CharField(required=False,
                                             widget=forms.HiddenInput,
                                             label="leave empty",
                                             validators=[must_be_empty])

    # overrides this field clean method in is_valid
    #its not a good way
    # def clean_honeypot_for_bot_check(self):
    #     honeypot_for_bot_check = self.cleaned_data['honeypot_for_bot_check']
    #     if len(honeypot_for_bot_check) > 0:
    #         raise forms.ValidationError("Bad bot,,...dont inspect me")
    #     print ("here", len(honeypot_for_bot_check))
    #     return honeypot_for_bot_check

    # override the complete clean method of form ,
    # do futher validation at one place for all fields
    def clean(self):
        cleaned_data = super().clean()