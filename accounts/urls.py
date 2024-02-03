from django.urls import path
from .views import PassWordChange,UserRegistrationView,UserLogOut,UserLoginView,UserBankAccountUpdateView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('logout/',UserLogOut,name='logout'),
    path('profile/', UserBankAccountUpdateView.as_view(), name='profile'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('changePass/',PassWordChange.as_view(),name='changePass')
]
