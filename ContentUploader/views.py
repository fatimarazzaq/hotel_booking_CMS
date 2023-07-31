from typing import Dict
from django.shortcuts import redirect, render,HttpResponse
from users.decorators import customer_required,administrator_required,hallmanager_required,admin_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView,UpdateView,DeleteView
from .models import MarriageHall,HallImages,HallVideos
from django.contrib import messages
from django.utils.decorators import method_decorator
from users.models import Customer,Administrator,HallManager,User
from django.db.models import Q
from bookings.models import Booking




# Create your views here.

def index(request):
    location=request.GET.get('location')
    if location:
        location = location.lower()
        all_hall_on_location=MarriageHall.objects.filter(
            Q(location__icontains=location) |
            Q(title__icontains=location) |
            Q(description__icontains=location)).all()
        if not all_hall_on_location:
            messages.success(request,f'{location} is not listed yet :(. Please search another!')
            return redirect('home')
        context={'location':location,'all_hall_on_location':all_hall_on_location}
        return render(request,'ContentUploader/hall_list_on_location.html',context)
    
    

    return render(request,'ContentUploader/index.html')




@administrator_required
def administrator_dashboard(request):
    all_halls=MarriageHall.objects.all()
    all_hall_profiles=HallManager.objects.all()
    profile_with_no_hall=[]
    for profile in all_hall_profiles:
        if(profile.marriagehall_set.all().count()==0):
            profile_with_no_hall.append(profile)

    context={
            'all_halls':all_halls,
            'profile_with_no_hall':profile_with_no_hall,
        }
    return render(request,'ContentUploader/administrator_dashboard.html',context)




@hallmanager_required
def hall_dashboard(request):
    ahfcu=MarriageHall.objects.filter(owner=request.user.hallmanager).all()
    manager = HallManager.objects.filter(user=request.user).first()
    context={
        'a_halls_fcu':ahfcu,
        'manager':manager,
    }
    return render(request,'ContentUploader/hallmanager_dashboard.html',context)


@customer_required
def customer_dashboard(request):
    customer=Customer.objects.filter(user=request.user).first()
    _customer_bookings=Booking.objects.filter(customer=customer).all()
    context={
        'all_cus_bookings':_customer_bookings,
    }
    return render(request,'ContentUploader/customer_dashboard.html',context)



       

@admin_required
def admin_dashboard(request):
    all_hall_managers=HallManager.objects.all()
    all_administrators=Administrator.objects.all()
    all_bookings=Booking.objects.all()
    all_marriage_halls=MarriageHall.objects.all()
    
    context={
        'all_hall_managers':all_hall_managers,
        'all_administrators':all_administrators,
        'all_bookings':all_bookings,
        'all_marriage_halls':all_marriage_halls,
    }

    return render(request,'ContentUploader/admin_dashboard.html',context)



@method_decorator(administrator_required, name='dispatch')
class HallCreationView(LoginRequiredMixin,CreateView):
    model = MarriageHall
    fields=['title','description','location','price','owner']
    template_name = 'ContentUploader/create_hall.html'

    def form_valid(self,form):
        return super().form_valid(form)
    

@administrator_required
def upload_hall_content(request,pk):
    marriage_hall=MarriageHall.objects.filter(id=pk).first()
    marr_img_alt=marriage_hall.title
    if(request.method=='POST'):
        images=request.FILES.getlist('images')
        for image in images:
            img=HallImages.objects.create(image=image,image_alt=marr_img_alt,hall=marriage_hall)
            img.save()
        videos=request.FILES.getlist('videos')
        for video in videos:
            vid=HallVideos.objects.create(video=video,hall=marriage_hall)
            vid.save()
        return redirect('hall-detail',pk=marriage_hall.id)
    context={
        'object':marriage_hall,
        'videos':marriage_hall.hallvideos_set.all(),
        'images':marriage_hall.hallimages_set.all(),
    }
    return render(request,'ContentUploader/marriage_hall_detail.html',context)




def HallDetailView(request,pk):
    marriagehall=MarriageHall.objects.filter(pk=pk).first()
    context={
        'marriagehall':marriagehall,
    }
    return render(request,'ContentUploader/marriage_hall_detail.html',context)



@administrator_required
def deletehallimage(request):
    if request.method=='POST':
        try:
            image_str=request.POST.get('delimage')
            getImage=HallImages.objects.get(id=int(image_str))
            hall=getImage.hall
            getImage.delete()
        except Exception as e:
            messages.success(request,f'Technical Error occured')
        return redirect('hall-detail',pk=hall.id)
    # return redirect('home')
    return render(request,'ContentUploader/index.html')

@administrator_required
def deletehallvideo(request):
    if request.method=='POST':
        try:
            video_str=request.POST.get('delvid')
            getVideo=HallVideos.objects.get(id=int(video_str))
            hall=getVideo.hall
            getVideo.delete()
        except Exception as e:
            messages.success(request,f'Technical Error occured')
        return redirect('hall-detail',pk=hall.id)
    # return redirect('home')
    return render(request,'ContentUploader/index.html')


@method_decorator(administrator_required, name='dispatch')
class HallUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = MarriageHall
    fields=['title','description','location','price']
    template_name = 'ContentUploader/create_hall.html'    
    
    def form_valid(self,form):
        form.instance.administrator=self.request.user.administrator
        return super().form_valid(form)
    
    def test_func(self):
        hall=self.get_object()
        if self.request.user.administrator==hall.administrator:
            return True
        return False



@method_decorator(administrator_required, name='dispatch')
class HallDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = MarriageHall
    template_name = 'ContentUploader/marriage_hall_delete.html'
    success_url='/'
    def test_func(self):
        hall=self.get_object()
        if self.request.user.administrator==hall.administrator:
            return True
        return False
    


@admin_required
def deleted_by_admin(request,rolename,id):
    if request.user.is_admin:
        if rolename == "administrator":
            tobedeleted = User.objects.get(id=id)
            if tobedeleted:
                messages.success(request,f'{tobedeleted.user.username} deleted successfully!')
                tobedeleted.delete()
                return redirect("admin_dashboard")
        elif rolename == "hallmanager":
            tobedeleted = User.objects.get(id=id)
            if tobedeleted:
                messages.success(request,f'{tobedeleted.user.username} deleted successfully!')
                tobedeleted.delete()
                return redirect("admin_dashboard")
        
        elif rolename == "booking":
            tobedeleted = Booking.objects.get(id=id)
            if tobedeleted:
                messages.success(request,f'{tobedeleted} deleted successfully!')
                tobedeleted.delete()
                return redirect("admin_dashboard")
        elif rolename == "marHall":
            tobedeleted = Booking.objects.get(id=id)
            if tobedeleted:
                messages.success(request,f'{tobedeleted.title} deleted successfully!')
                tobedeleted.delete()
                return redirect("admin_dashboard")

    
    return HttpResponse("DONE")