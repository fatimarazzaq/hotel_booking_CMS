from django import forms
from django.forms import fields
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Administrator,User,HallManager,Customer


class HallManagerSignupForm(UserCreationForm):
    phone_number = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Whatsapp number e.g 923124436231'}))

    class Meta(UserCreationForm.Meta):
        model=User
        fields = ['username','email','password1','password2','phone_number']
    
    def clean(self):
        super(HallManagerSignupForm, self).clean()

        ph_number = self.cleaned_data.get('phone_number')

        if len(ph_number) < 12 or len(ph_number) > 12:
            self._errors['phone_number'] = self.error_class(['Phone number is not valid'])

        if not ph_number.isnumeric():
            self._errors['phone_number'] = self.error_class(['Phone number is not valid'])

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_hall_manager =True
        user.save()
        hallmanager = HallManager.objects.create(user=user)
        hallmanager.phone_number = str(self.cleaned_data.get('phone_number'))
        hallmanager.save()
        return hallmanager

    

class AdministratorSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','password1','password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_administrator = True
        user.save()
        administrator=Administrator.objects.create(user=user)
        administrator.save()
        return administrator


class CustomerSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','password1','password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer=Customer.objects.create(user=user)
        customer.save()
        return customer








# profile forms


class ProfileImageUpdationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']


# hall manager