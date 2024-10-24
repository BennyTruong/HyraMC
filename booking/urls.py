from django.urls import path
from booking import views

urlpatterns = [
    
    path('create/', views.create_booking, name='create_booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('list/', views.booking_list, name='booking_list'),
    path("", views.home, name="home"),
]
