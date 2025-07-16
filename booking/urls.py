from django.urls import path
from booking import views

urlpatterns = [
    
    path('create/', views.create_booking, name='create_booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('list/', views.booking_list, name='booking_list'),
    path('price/', views.price, name='price'), 
    path('contact/', views.contact, name='contact'),
    path('contact_submit/', views.contact_submit, name='contact_submit'),
    path('contact_success/', views.contact_success_view, name='contact_success'),
    path('add_review/', views.add_review, name='add_review'),
    path('rentalpolicy/', views.rentalpolicy, name='rentalpolicy'),
    path("", views.home, name="home"),
]
