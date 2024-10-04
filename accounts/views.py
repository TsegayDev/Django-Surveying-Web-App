from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.models import Group

def sign_out(request):
  logout(request)
  return redirect('/accounts/sign_in/')
  
def sign_in(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/home/')
        else:
            return redirect('/home')
    
    elif request.method == "POST":
        username_or_email = request.POST.get('input_email')
        password = request.POST.get('input_password')
        
        # Attempt to authenticate by username or email
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            user = authenticate(request, email=username_or_email, password=password)
        
        if user is not None:
            login(request, user)

            # Check user role and redirect accordingly
            if user.groups.filter(name='Admin').exists():
                return redirect('/home/')
            elif user.groups.filter(name='Editor').exists():
                return redirect('/editor_dashboard/')
            else:
                return redirect('/')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('/accounts/sign_in/')
    
    return render(request, 'sign_in.html', {'page_title': "Zalla | Sign In"})
    
    
def sign_up(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/home/')
        else:
            return redirect('/home')

    elif request.method == 'POST':
        form_data = request.POST
        email = form_data.get('input_email')
        
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken!")
        else:
            password = form_data.get('input_pass1')
            password_confirm = form_data.get('input_pass2')
            
            if password == password_confirm:
                user = User.objects.create_user(
                    first_name=form_data.get('input_fname'),
                    last_name=form_data.get('input_lname'),
                    email=email
                )
                user.set_password(password)
                user.save()
                
                # Automatically log in the user
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Account created and logged in successfully!")
                    # Redirect based on user group
                    if user.is_superuser:
                        return redirect('/home/')
                    else:
                        return redirect('/home')
            else:
                messages.error(request, "Password mismatched")
    
    return render(request, 'sign_up.html', {'page_title': "Zalla | Sign Up"})
