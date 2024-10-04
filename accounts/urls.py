from django.urls import path
from accounts.views import *

urlpatterns = [
    path('accounts/sign_in/', sign_in, name='sign_in'),
    path('accounts/sign_up/', sign_up, name='sign_up'),
    path('accounts/sign_out/', sign_out, name='sign_out'),
]
