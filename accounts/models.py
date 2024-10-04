from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_hashids import HashidsField

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin):
    hashid = HashidsField(real_field_name='id')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100,)
    password = models.CharField(max_length=128,)
    password2 = models.CharField(max_length=128, default='temporary_password')
    profile_photo = models.ImageField(upload_to='user-profiles/', default="user-profiles/default-profile.jpg")
    added_on = models.DateTimeField(default=timezone.now,)
    updated_on = models.DateTimeField(auto_now=True,)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','password']
    def __str__(self):
        return self.email
    class Meta:
        ordering = ['email']
        verbose_name = "User"
        verbose_name_plural = "Users"