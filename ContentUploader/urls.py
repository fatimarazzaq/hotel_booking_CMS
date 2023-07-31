
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='home'),
    # path('hall_list/<str:location>/',views.hall_on_location,name='hall_on_location'),
    path('dashboard/administrator/',views.administrator_dashboard,name='administrator_dashboard'),
    path('dashboard/customer/',views.customer_dashboard,name='customer_dashboard'),
    path('dashboard/hall/',views.hall_dashboard,name='hall_dashboard'),
    path("detail/marriagehall/<int:pk>/",views.HallDetailView,name='hall-detail'),
    path("marriagehall/<int:pk>/update/",views.HallUpdateView.as_view(),name='hall-update'),
    path("marriagehall/<int:pk>/delete/",views.HallDeleteView.as_view(),name='hall-delete'),
    path('admin/dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path("upload/marriagehall/content/",views.HallCreationView.as_view(),name='create-hall'),
    path("marriagehall/content/<int:pk>/",views.upload_hall_content,name='upload-content'),
    path("marriagehall/content/delete/image",views.deletehallimage,name='hall-image-delete'),
    path("marriagehall/content/delete/video",views.deletehallvideo,name='hall-video-delete'),


    # deleted by admin

    path("admin/delete/<str:rolename>/<int:id>/",views.deleted_by_admin,name="deleted_by_admin")
]