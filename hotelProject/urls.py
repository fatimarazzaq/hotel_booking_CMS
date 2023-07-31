"""hotelProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include,re_path
from bookings import views as booking_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ContentUploader.urls')),
    path('accounts/',include('users.urls')),
    
    path("marriagehall_booking/<int:pk>/",booking_views.HallBookingOnLocation,name='hall-booking'),
    path('set_custom_booking/<int:pk>/',booking_views.SetCustomBooking,name='set_custom_booking'),
    path('set_custom_booking/new_customer/<int:pk>/',booking_views.SetCusBookWithNcust,name='set_custom_booking_with_ncustomer'),
    path('set_custom_booking/exsisting_customer/<int:pk>/',booking_views.SetCusBookWithEcust,name='set_custom_booking_with_ecustomer'),    

    path('check_user/',booking_views.check_user,name='check_user'),
    path('check_customer_user/',booking_views.check_customer_user,name='check_customer_user'),
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)