from django.contrib import admin

# Register your models here.
from .models import User, Profile, Dealer

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Dealer)