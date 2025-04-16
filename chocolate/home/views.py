from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.

def app(request):
    return render(request, 'index.html')

def exit(request):
    logout(request)
    return redirect('app')

def register(request):
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(
                username=user_creation_form.cleaned_data['username'],
                password=user_creation_form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('app')
    else:
        user_creation_form = CustomUserCreationForm()

    context = {
        'form': user_creation_form,
        'titulo': "Register",
        'contents': {
            'username': user_creation_form['username'],
            'first_name': user_creation_form['first_name'],
            'last_name': user_creation_form['last_name'],
            'email': user_creation_form['email'],
            'password1': user_creation_form['password1'],
            'password2': user_creation_form['password2'],
        },
        'content_botton': "Sign in"
    }

    return render(request, 'registration/register.html', context)

@login_required
def profile(request):
    user_form = CustomUserChangeForm(instance=request.user)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(profile)
    
    context = {
        'form': user_form,
        'titulo': "Perfil",
        'contents': {
            'username': user_form['username'],
            'first_name': user_form['first_name'],
            'last_name': user_form['last_name'],
            'email': user_form['email'],
        },
        'content_button': "editing",
        'title_button': "Change password",
        'href': "change-password",
    }
    return render(request, 'profile.html', context)

