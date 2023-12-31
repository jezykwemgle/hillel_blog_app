from blog.tasks import contact_us

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

from user_management.forms import ContactUs, RegisterForm


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    """
    Профіль залогіненого юзера.
    """
    model = User
    template_name = 'registration/profile.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserEditProfileView(LoginRequiredMixin, generic.UpdateView):
    """
    Редагування профілю залогіненого юзера.
    """
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = 'registration/edit_profile.html'
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse_lazy('accounts:my-profile')


class RegisterFormView(generic.FormView):
    """
    Реєстрація нового юзера, якщо реєстрація успішна - логін юзера.
    """
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:my-profile")

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class ContactUsView(generic.FormView):
    """
    Зв'язок з адміном.
    """
    template_name = 'registration/contact_us.html'
    form_class = ContactUs
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        contact_us.delay(form.cleaned_data.get('subject'),
                         form.cleaned_data.get('message'),
                         form.cleaned_data.get('email'))
        return super(ContactUsView, self).form_valid(form)
