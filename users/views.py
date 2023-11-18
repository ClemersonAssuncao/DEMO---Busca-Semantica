from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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

def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()
        email_v = User.objects.filter(email=email).first()

        if user:
            return render(request, 'users/signup.html', {'Error': 'Já existe um usuário com esse nome.'})
        if email_v:
            return render(request, 'users/signup.html', {'Error': 'Já existe um usuário com esse email.'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect("users:login")

    else:
        return render(request, 'users/signup.html')

def password_user(request):
    return render(request, 'users/password_reset.html')
