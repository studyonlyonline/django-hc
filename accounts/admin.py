from django.contrib import admin

# Register your models here.
from .models import User, Profile, Dealer

admin.register(User)
admin.register(Profile)
admin.register(Dealer)