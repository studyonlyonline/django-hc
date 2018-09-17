from django.http import HttpResponse
from django.shortcuts import render
from .models import Schemes

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def schemes_list(request):
    schemes = Schemes.objects.filter(is_active=True)
    context = {
        'schemes_list' : schemes
    }
    print("schemes ",schemes)
    return render(request=request, template_name='home_module/schemes_list.html', context=context)