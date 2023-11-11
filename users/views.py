from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_user(request):
    
    if request.user.is_authenticated:
        return redirect("index")

    if request.POST:
        user = authenticate(username= request.POST.get("username", ""), password= request.POST.get("password", ""))

        if user is not None:
            login(request, user)
            return redirect("search:index")
        else:
            return render(request, 'users/login.html', {'Error': 'Usuário ou senha inválido!'})

    return render(request, 'users/login.html')

@login_required(redirect_field_name="users:login")
def logout_user(request):

    if request.POST:
        logout(request)
        return redirect("search:index")

    return render(request, 'users/logout.html')

def password_user(request):
    return render(request, 'users/password_reset.html')
