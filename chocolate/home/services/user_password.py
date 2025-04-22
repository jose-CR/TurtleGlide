from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib import messages

#variables template
template_password = 'profile/password/'

class UserPasswordChange(PasswordChangeView):
    template_name = f"{template_password}change-password.html"
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "La contraseña se ha cambiado exitosamente.")
        return super().form_valid(form)

class UserPasswordReset(PasswordResetView):
        template_name = f"{template_password}reset_password_email.html"
        success_url = reverse_lazy('profile')
        email_template_name = f"{template_password}password_reset_email.html"

        def form_valid(self, form):
            messages.success(self.request, "Se ha enviado un correo electrónico a tu bandeja de entrada.")
            return super().form_valid(form)

class UserPasswordConfirm(PasswordResetConfirmView):
        template_name = f"{template_password}reset_confirm.html"
        success_url = reverse_lazy('reset-password-done')

class UserPasswordComplete(PasswordResetCompleteView):
    template_name = f"{template_password}reset_password_complete.html"
