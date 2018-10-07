from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.http import HttpResponse
from . import forms

def send_contact_lead(form_data):
    response = send_mail(
        subject="Contact form".format(form_data['name']),
        message=form_data['message'],
        from_email='{name} {email}'.format(**form_data),
        recipient_list=['sarthak937gupta@gmail.com']
    )
    return response

def contact_form_view(request):
    form = forms.ContactForm()
    if request.method == 'POST':
        form = forms.ContactForm(data=request.POST)
        if form.is_valid():
            response = send_contact_lead(form.cleaned_data)
            # mail sent successfully
            if response == 1:
                messages.add_message(request=request, level=messages.SUCCESS, message="We will contact soon")
            else:
                messages.add_message(request=request, level=messages.ERROR, messages="Some error occured")
            return HttpResponseRedirect(reverse('index_page'))

    context = {
        'form': form
    }
    return render(request=request, template_name='contact_form.html', context=context)

class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("Hello world")

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['games'] = 6
        print ("Context  ",context)
        return context
