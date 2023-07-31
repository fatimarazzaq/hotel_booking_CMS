
from django import forms




class CustomLoginForm(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Username'}))




class BookingForm(forms.Form):
    check_in = forms.DateTimeField(required=True,input_formats=["%Y-%m-%dT%H:%M",])
    check_out = forms.DateTimeField(required=True,input_formats=["%Y-%m-%dT%H:%M",])