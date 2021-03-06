from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.db import models
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,email,username, display_name=None, password = None):
        if not email:
            raise ValueError("User must have an email address")

        if not display_name:
            display_name = username


        user  = self.model(
                email = self.normalize_email(email),
                username = username,
                display_name = display_name
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, display_name, password):
        user = self.create_user(
            username = username,
            email = email,
            display_name = display_name,
            password = password
        )
        user.is_staff  = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    display_name = models.CharField(max_length=140)
    bio = models.CharField(max_length=140, blank=True, default="")
    # avatar = models.ImageField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['display_name', 'username']

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.display_name

    def get_long_name(self):
        return "{} (@{})".format(self.display_name, self.username)

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.IntegerField(blank=False)
    delivery_address = models.TextField(blank = False)
    apply_for_dealership = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " " + str(self.contact_no)

class Dealer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gstin = models.CharField(blank=True, max_length=15)
    company_name = models.TextField(blank=False)