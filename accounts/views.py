from django.shortcuts import redirect, render
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView,LoginView
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'accounts/ user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)


class UserLogOutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self) -> str:
        return reverse_lazy('home')