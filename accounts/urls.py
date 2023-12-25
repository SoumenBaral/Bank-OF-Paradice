from django.urls import path
from .views import UserRegistrationView,UserLogOutView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('logout/',UserLogOutView.as_view(),name='logout')
]
