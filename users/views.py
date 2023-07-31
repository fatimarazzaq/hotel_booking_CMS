from django.shortcuts import render,redirect
from .forms import CustomerSignupForm,AdministratorSignupForm,HallManagerSignupForm,ProfileImageUpdationForm
from django.contrib import messages
from django.http import JsonResponse
from .decorators import admin_required
from django.conf import settings
from django.core.mail import send_mail
from .models import Customer,User,Administrator,HallManager
import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
import pytz


utc=pytz.UTC



# Create your views here.
def CustomerUserRegister(request):
    if request.method=='POST':
        form=CustomerSignupForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            messages.success(request, f'{username} ,verify your account to proceed further.')
            form.save()
            email=form.cleaned_data['email']
            user=User.objects.filter(email=email).first()
            customer=Customer.objects.filter(user=user).first()
            auth_token=uuid.uuid4()
            customer.auth_token=auth_token
            customer.save()
            send_mail_after_registration(email,auth_token,user)
            return redirect('/accounts/register/verification_token/')
        else:
            messages.success(request, f'Your username or email is incorrect. Try another')
            return redirect('/accounts/customer_register/')
            

    form=CustomerSignupForm()
    return render(request,'users/customer_register.html',{'form':form})






@admin_required
def AdministratorUserRegister(request):
    if request.method=='POST':
        form=AdministratorSignupForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            messages.success(request, f'{username} is created as an administrator,Verify this account to proceed further.')
            form.save()
            email=form.cleaned_data['email']
            user=User.objects.filter(email=email).first()
            administrator=Administrator.objects.filter(user=user).first()
            auth_token=uuid.uuid4()
            administrator.auth_token=auth_token
            administrator.save()
            send_mail_after_registration(email,auth_token,user)
            return redirect('/accounts/register/verification_token/')
        else:
            messages.success(request, f'Your username or email is incorrect. Try another')
            return redirect('/accounts/administrator_register/')

    form=AdministratorSignupForm()
    return render(request,'users/administrator_register.html',{'form':form})




@admin_required
def HallUserRegister(request):
    if request.method=='POST':
        form=HallManagerSignupForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            # phone_number = form.cleaned_data['phone_number']
            # if len(phone_number)!=11:
            #     messages.success(request,f'{username} please enter a valid phone number')
            #     return redirect('/accounts/hall_register/')
            form.save()
            messages.success(request,f'{username} is created as an Hall Manager.Verify this account to proceed further.')
            email=form.cleaned_data['email']
            user=User.objects.filter(email=email).first()
            hallmanager=HallManager.objects.filter(user=user).first()
            
            auth_token=uuid.uuid4()
            hallmanager.auth_token=auth_token
            hallmanager.save()
            send_mail_after_registration(email,auth_token,user)
            return redirect('/accounts/register/verification_token/')
        # else:
        #     messages.success(request, f'Your data is not valid . Try again.')
        #     return redirect('/accounts/hall_register/')

    form=HallManagerSignupForm()
    return render(request,'users/hall_register.html',{'form':form})





def verification_info(request):
    return render(request,'users/verification_info.html')

def verification_success(request):
    return render(request,'users/verification_success.html')

def verify(request,auth_token,id):
    try:
        user=User.objects.filter(id=id).first()
        if user.is_customer:
            customer=Customer.objects.filter(auth_token=auth_token).first()
            if customer:
                if customer.is_verified:
                    messages.success(request, f'Hey {customer.user.username}, you are already verified . ')
                    return redirect('/accounts/login/')
                else:
                    customer.is_verified=True
                    customer.save()
                    messages.success(request, f'Hey {customer.user.username},your account is verified Successfully.')
                    return redirect('/accounts/login/')
        elif user.is_administrator:
            administrator=Administrator.objects.filter(auth_token=auth_token).first()
            if administrator:
                if administrator.is_verified:
                    messages.success(request, f'Hey {administrator.user.username}, you are already verified . ')
                    return redirect('/accounts/login/')
                else:
                    administrator.is_verified=True
                    administrator.save()
                    messages.success(request, f'Hey {administrator.user.username},your account is verified Successfully.')
                    return redirect('/accounts/login/')
        elif user.is_hall_manager:
            hallmanager=HallManager.objects.filter(auth_token=auth_token).first()
            if hallmanager:
                if hallmanager.is_verified:
                    messages.success(request, f'Hey {hallmanager.user.username}, you are already verified . ')
                    return redirect('/accounts/login/')
                else:
                    hallmanager.is_verified=True
                    hallmanager.save()
                    messages.success(request, f'Hey {hallmanager.user.username},your account is verified Successfully.')
                    return redirect('/accounts/login/')
        
        
    except Exception as e:
        return redirect('home')



def send_mail_after_registration(email,token,user):
    subject="Your Account Need to be Verified"
    message=f"Hi paste the link to verify your account http://127.0.0.1:8000/accounts/verify/{token}/{user.id}/"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list,fail_silently=True)




# Profile updation forms

@login_required
def profile(request):

    if request.method == 'POST':
        i_form = ProfileImageUpdationForm(request.POST,request.FILES,instance=request.user)
        if i_form.is_valid():
            i_form.save()
            return redirect('profile')

    i_form = ProfileImageUpdationForm(instance=request.user)

    context={
            'i_form':i_form,
        }
    return render(request,'users/profile.html',context)