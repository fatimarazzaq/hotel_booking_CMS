from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('customer_register/',views.CustomerUserRegister,name='customer_register'),
    


    path('administrator_register/',views.AdministratorUserRegister,name='administrator_register'),
    path('hall_register/',views.HallUserRegister,name='hall_register'),
    path('register/verification_token/',views.verification_info,name='verification_info'),
    path('verify/<auth_token>/<int:id>/',views.verify,name='verify'),
    path('profile/',views.profile,name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),

    # password reset routes
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
]
