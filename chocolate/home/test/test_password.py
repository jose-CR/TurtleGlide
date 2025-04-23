from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.messages import get_messages
from home.utils.test_helpers import call_status
from django.contrib.auth.models import User

# Create your tests here.
class TestPasswordUser(TestCase):
    #variables templates
    template_password = 'profile/password/'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="usuario_password", password="ContraseñaVieja123", email="usuario@email.com")
        self.client.login(username="usuario_password", password="ContraseñaVieja123")

    def test_user_change_password(self):
        template_password_change = f"{self.template_password}change-password.html"
        url = reverse('change-password')

        try:
            response_get = self.client.get(url)
            self.assertEqual(response_get.status_code, 200)
            self.assertTemplateUsed(response_get, template_password_change)

            data = {
                "old_password": "ContraseñaVieja123",
                "new_password1": "ContraseñaNueva456",
                "new_password2": "ContraseñaNueva456"
            }

            response_post = self.client.post(url, data, follow=True)
            self.assertRedirects(response_post, reverse('profile'))

            self.client.logout()
            login_success = self.client.login(username="usuario_password", password="ContraseñaNueva456")
            self.assertTrue(login_success)
            messages = list(get_messages(response_post.wsgi_request))   
            self.assertTrue(any("La contraseña se ha cambiado exitosamente." in str(m) for m in messages))

            call_status(
                response=response_post,
                url_name=url,
                expected_status=200,
                message="contraseña cambiada correctamente"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_CHANGE] - {str(e)}")
            self.fail(f"Falló al testear el cambio de contraseña: {e}")

    def test_user_reset_password(self):
        template_password_reset = f"{self.template_password}reset_password_email.html"
        url = reverse('reset-password')

        try:
            response_get = self.client.get(url)
            self.assertEqual(response_get.status_code, 200)
            self.assertTemplateUsed(response_get, template_password_reset)

            data = {"email": self.user.email}
            response_post = self.client.post(url, data, follow=True)

            self.assertRedirects(response_post, reverse('profile'))
            messages = list(get_messages(response_post.wsgi_request))
            self.assertTrue(any(
                "Se ha enviado un correo electrónico a tu bandeja de entrada." in str(m)
                for m in messages
            ))

            self.assertEqual(len(mail.outbox), 1)
            self.assertIn(self.user.email, mail.outbox[0].to)

            call_status(
                response=response_post,
                url_name=url,
                expected_status=200,
                message="solicitud de restablecimiento de contraseña exitosa"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_RESET] - {str(e)}")
            self.fail(f"Falló al testear el restablecimiento de contraseña: {e}")            

    def test_user_confirm_password(self):
        template_password_confirm = f"{self.template_password}reset_confirm.html"
        url = reverse('reset-password-done')
        try:
            # GET request
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            call_status(
                response=response,
                url_name=url,
                expected_status=200,
                message="confirmación de restablecimiento de contraseña exitosa"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_CONFIRM] - {str(e)}")
            self.fail(f"Falló al testear el restablecimiento de contraseña: {e}")

    def test_user_complete_change_password(self):
        try:
            template_password_complete = f"{self.template_password}reset_password_complete.html"
            
            # Obtener la URL real usando el `name` de la ruta
            url = reverse('reset-password-done')

            # Hacer GET request
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_password_complete)

            call_status(
                response=response,
                url_name=template_password_complete,
                expected_status=200,
                message="renderización del template de finalización de cambio de contraseña"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_COMPLETE] - {str(e)}")
            self.fail(f"Falló al testear el render del password complete: {e}")

