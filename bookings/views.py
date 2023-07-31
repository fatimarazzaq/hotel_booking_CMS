from django.shortcuts import render,redirect
from .models import Booking
from django.contrib.auth.decorators import login_required
from ContentUploader.models import MarriageHall
from bookings.booking_functions import availability
from datetime import datetime
from users.models import Customer,HallManager,User
from django.contrib import messages
from .forms import CustomLoginForm
from users.forms import CustomerSignupForm
from django.http.response import JsonResponse
from users.decorators import hallmanager_required

import pytz

utc=pytz.UTC


# Create your views here.



@login_required
def HallBookingOnLocation(request,pk):
    marriagehall=MarriageHall.objects.filter(pk=pk).first()
    if request.method=='POST':  
        checkin=request.POST.get('checkin')
        checkout=request.POST.get('checkout')
        check_in=utc.localize(datetime.strptime(checkin,'%Y-%m-%dT%H:%M'))
        check_out=utc.localize(datetime.strptime(checkout,'%Y-%m-%dT%H:%M'))
        user = request.user
        customer = Customer.objects.filter(user=user).first()

        if check_in < check_out:
            available= availability.avail_func(marriagehall,check_in,check_out)
            if available:
                        # create booking
                book = Booking.objects.create(marriagehall=marriagehall,customer=customer,check_in=check_in,check_out=check_out)
                book.save()
                messages.success(request, f'Booking for {customer.user.username} is created successfully. ')
                return redirect('hall-detail',pk=marriagehall.id)
                        
            else:
                messages.success(request, f'Hey , the check-in or check-out dates you entered are already booked. Please try another time frame for your event.')
                return redirect('hall-detail',pk=marriagehall.id)
                
        else:
            messages.success(request, f'Check-in date must be less than check-out dates')
        return redirect('hall-detail',pk=marriagehall.id)
            
    context={
        'marriagehall':marriagehall,
    }
    return render(request,'ContentUploader/marriage_hall_detail.html',context)





@hallmanager_required
def SetCustomBooking(request,pk):
    context={'managerID':pk}
    return render(request,'bookings/set_custom_booking.html',context)



@hallmanager_required
def SetCusBookWithEcust(request,pk):
    id=int(pk)
    hallmanager=HallManager.objects.filter(id=id).first()
    halls_list_of_this_manager = MarriageHall.objects.filter(owner=hallmanager).all()
    if request.method=='POST':
        checkiny = request.POST.get('checkin')
        checkouty = request.POST.get('checkout')

        # checking availability
        checkin=checkiny
        checkout= checkouty
        check_in=utc.localize(datetime.strptime(checkin,'%Y-%m-%dT%H:%M'))
        check_out=utc.localize(datetime.strptime(checkout,'%Y-%m-%dT%H:%M'))


        username = request.POST.get("username")
        user = User.objects.filter(username=username).first()

        hallid=int(request.POST.get('marriage_hall'))
        marriagehall = MarriageHall.objects.get(id=hallid)


        if user:
            customer = Customer.objects.filter(user=user).first()
            if check_in < check_out:
                available_or_not = availability.avail_func(marriagehall,check_in,check_out)
                if available_or_not:
                        # create booking
                    book = Booking.objects.create(marriagehall=marriagehall,customer=customer,check_in=check_in,check_out=check_out)
                    book.save()
                    messages.success(request, f'Booking for {customer.user.username} is created successfully. ')
                    return redirect('hall_dashboard')   
                else:
                    messages.success(request, f'The Check-in and Check-out dates you entered are already booked . Please try another time frame for your event.')
                    return redirect('set_custom_booking_with_ecustomer', pk=id)

            else:
                messages.success(request, f'Check in date must be less than check out date.')
                return redirect('set_custom_booking_with_ecustomer', pk=id)
        else:
            messages.success(request, f'{username} not found . Please create new Customer to set his/her booking.')
            return redirect('set_custom_booking',pk=pk)

    e_cust_form = CustomLoginForm() 
    context={'e_cust_form':e_cust_form,'myhalls':halls_list_of_this_manager,'managerID':pk}
    return render(request,'bookings/exsis_cus_with_book.html',context)




def check_customer_user(request):
    if request.method == 'POST':
        username = request.POST['musername']
        user = User.objects.filter(username=username).first()
        if(user and user.is_customer):
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})
    else:
        return JsonResponse({'status':False})


def check_user(request):
    if request.method == 'POST':
        username = request.POST['musername']
        user = User.objects.filter(username=username).first()
        if(user):
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})
    else:
        return JsonResponse({'status':False})






@hallmanager_required
def SetCusBookWithNcust(request,pk):
    id=int(pk)
    hallmanager=HallManager.objects.filter(id=id).first()
    halls_list_of_this_manager = MarriageHall.objects.filter(owner=hallmanager).all()
    if request.method=='POST':
        hallid=int(request.POST.get('marriage_hall'))
        marriagehall = MarriageHall.objects.get(id=hallid)
        checkiny = request.POST.get('checkin')
        checkouty = request.POST.get('checkout')

        # checking availability
        checkin=checkiny
        checkout= checkouty
        check_in=utc.localize(datetime.strptime(checkin,'%Y-%m-%dT%H:%M'))
        check_out=utc.localize(datetime.strptime(checkout,'%Y-%m-%dT%H:%M'))

        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        # finding customer
        if user:
            messages.success(request, f'The username You entered already exsists')
            return redirect('set_custom_booking_with_ecustomer',pk=pk)
        else:
            c_form = CustomerSignupForm(request.POST)
            if c_form.is_valid():
                c_form.save()

            email = c_form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            customer = Customer.objects.filter(user=user).first()

            if check_in < check_out:
                available_or_not= availability.avail_func(marriagehall,check_in,check_out)
                if available_or_not:
                        # create booking
                    book = Booking.objects.create(marriagehall=marriagehall,customer=customer,check_in=check_in,check_out=check_out)
                    book.save()
                    messages.success(request, f'Booking for {customer.user.username} is created successfully. ')
                    return redirect('hall_dashboard')   
                else:
                    messages.success(request, f'The Check-in and Check-out dates you entered are already booked . Please try another time frame for your event.')
            
                    return redirect('set_custom_booking_with_ncustomer', pk=id)

            else:
                messages.success(request, f'Check in date must be less than check out date.')
                return redirect('set_custom_booking_with_ncustomer', pk=id)


    c_form=CustomerSignupForm()
    context={'c_form':c_form,'myhalls':halls_list_of_this_manager,'managerID':pk}
    return render(request,'bookings/crea_new_cus_with_book.html',context)