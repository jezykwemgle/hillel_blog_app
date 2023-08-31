from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


class UserProfileView(LoginRequiredMixin, generic.DetailView):
   model = User
   template_name = 'registration/profile.html'

   def get_object(self, queryset=None):
       user = self.request.user
       return user


# TODO: зробити можливість редагування профілю тільки для юзеру який залогінився
class UserEditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = 'registration/edit_profile.html'
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse_lazy('accounts:profile')
