from home.forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create perfil
class ProfileCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('app')

    def form_valid(self, form):
        self.object = form.save()
        success_url = reverse_lazy('app')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            
        return redirect(success_url)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['button'] = 'Sing In'
        return context

# Read perfil
class Profile():
    def exit(request):
        logout(request)
        return redirect('app')

    @login_required
    def index(request):

        context = {
            'label_username': 'Usuario',
            'label_first_name': 'Primer Nombre',
            'label_last_name': 'Último Apellido',
            'label_email': 'Correo Electrónico',
        }

        return render(request, 'profile.html', context)
    
# Update perfil
class ProfileUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'profile/profile-edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        response = super().get_object(queryset)
        user_id = self.kwargs.get('pk')
        if self.request.user.id == user_id:
            return self.request.user
        raise Http404("No puedes editar otro usuario.")

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Tu perfil se ha actualizado correctamente.')
        return response

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Edit User'
        context['button'] = 'editing'
        context['user_id'] = self.request.user.id
        return context
    
# Delete perfil 
class ProfileDeleteView(DeleteView):
    model = User
    template_name = 'profile/profile-delete.html'
    success_url = reverse_lazy('app')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)

        return response

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Delete User'
        context['button'] = 'deleting'
        return context
