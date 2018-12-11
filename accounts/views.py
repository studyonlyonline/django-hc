from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic, View
from . import forms
from django.shortcuts import render, redirect
from .models import Profile, Dealer

class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home_module:schemes_default_page")
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form=form)

class LogoutView(generic.RedirectView):
    url = reverse_lazy("home_module:schemes_default_page")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request=request,*args, **kwargs)

class SignUpView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class CreateProfile(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            data = Profile.objects.get(user = request.user)
            form = forms.ProfileForm(instance=data)
            print("in profiel get try")
        except Profile.DoesNotExist:
            form = forms.ProfileForm()
            print("in profiel get except")
        return render(request=request, template_name='accounts/profile.html', context={'form':form})

    def post(self, request, *args, **kwargs):
        try:
            profile_present = Profile.objects.get(user = request.user)
            form = forms.ProfileForm(instance=profile_present, data=request.POST)

            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated Profile")
            else:
                messages.add_message(request, messages.SUCCESS, "Profile Update failed")
            print("update profile")

        except Profile.DoesNotExist:
            form = forms.ProfileForm(data=request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                if request.user.is_authenticated:
                    profile.user = request.user
                    profile.save()
                    print("profile saved")
                    messages.add_message(request, messages.SUCCESS, "Profile created")
                elif request.user.is_anonymous:
                    messages.add_message(request, messages.SUCCESS, "Profile failed")
            else:
                messages.add_message(request ,messages.SUCCESS, "Form invalid")
                print("Create profile")
        return redirect(reverse_lazy('home_module:schemes_default_page'))

class DealerDetails(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        is_dealer = request.user.is_dealer
        form = {}
        try:
            if is_dealer:
                data = Dealer.objects.get(user = request.user)
                form = forms.DealerForm(instance=data)

        except Dealer.DoesNotExist:
            form = forms.DealerForm()

        context = {
            'form': form,
            'is_dealer': is_dealer
        }
        return render(request=request, template_name='accounts/dealer_details.html', context=context)

    def post(self, request, *args, **kwargs):
        try:
            dealer_present = Dealer.objects.get(user = request.user)
            if request.user.is_dealer:
                form = forms.DealerForm(instance=dealer_present, data=request.POST)

                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.SUCCESS, "Updated Dealer Details")
                else:
                    messages.add_message(request, messages.SUCCESS, "Dealer Details Update failed")
            else:
                messages.add_message(request, messages.SUCCESS, "You are not a dealer , Apply for it")

        except Dealer.DoesNotExist:
            if request.user.is_dealer:
                form = forms.DealerForm(data=request.POST)
                if form.is_valid():
                    dealer = form.save(commit=False)
                    if request.user.is_authenticated:
                        dealer.user = request.user
                        dealer.save()
                        messages.add_message(request, messages.SUCCESS, "Dealer created")
                    elif request.user.is_anonymous:
                        messages.add_message(request, messages.SUCCESS, "Dealer failed")

            else:
                messages.add_message(request, messages.SUCCESS, "You are not a dealer , Apply for it")

        return redirect(reverse_lazy('home_module:schemes_default_page'))
