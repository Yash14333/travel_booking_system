from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('travel/<int:pk>/', views.travel_detail, name='travel_detail'),
    path('travel/<int:pk>/book/', views.book_travel, name='book_travel'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<str:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
