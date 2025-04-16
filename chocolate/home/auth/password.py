from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib import messages

class PasswordViews:
    class Change(PasswordChangeView):
        template_name = "registration/password/change-password.html"
        success_url = reverse_lazy('profile')

        def form_valid(self, form):
            messages.success(self.request, "La contraseña se ha cambiado exitosamente.")
            return super().form_valid(form)

    class Reset(PasswordResetView):
        template_name = "registration/password/reset_password_email.html"
        success_url = reverse_lazy('profile')
        email_template_name = "registration/password/password_reset_email.html"

        def form_valid(self, form):
            messages.success(self.request, "Se ha enviado un correo electrónico a tu bandeja de entrada.")
            return super().form_valid(form)

    class Confirm(PasswordResetConfirmView):
        template_name = "registration/password/reset_confirm.html"
        success_url = reverse_lazy('reset-password-done')

    class Complete(PasswordResetCompleteView):
        template_name = "registration/password/reset_password_complete.html"
