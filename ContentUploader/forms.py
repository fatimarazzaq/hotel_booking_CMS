from django import forms
from .models import MarriageHall,Booking

class HallContentUploadingForm(forms.ModelForm):
    class Meta:
        model=MarriageHall
        fields=['title','description','location','price','owner']



