from django.test import TestCase, Client
from django.urls import reverse
from home.utils.test_helpers import template_use, call_status
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

# Create your tests here.

class ViewTests(TestCase):
    def test_app(self):
        url_name_index = 'app'
        try: 
            response = self.client.get(reverse('app'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_use(url_name_index))
            call_status(
                client=self.client,
                url_name=url_name_index,
                expected_status=200, 
                message="vista renderizada"
            )
        except Exception as e:
            print(f"❌ [ERROR EN {url_name_index.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{url_name_index}': {e}")

class ProfileCreateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_register_page(self):
        url_name = 'register'
        try:
            response = self.client.get(reverse(url_name))
            self.assertTemplateUsed(response, template_use(url_name))
            call_status(
                client=self.client,
                url_name=url_name,
                expected_status=200,
                message='Render de página de registro'
            )
        except Exception as e:
            print(f"❌ [ERROR EN {url_name.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{url_name}': {e}")

    def test_user_creation_and_login(self):
        url_name_index = 'app'
        url_name_register = 'register'

        user_data = {
            'username': 'nuevo_usuario',
            'password1': 'SuperSecreto123',
            'password2': 'SuperSecreto123',
        }

        try:
            response = self.client.post(reverse(url_name_register), user_data)
            call_status(
                url_name=url_name_register,
                response=response,
                expected_status=302,
                message="Usuario creado e insertado en la base de datos"
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse(url_name_index))

            self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())

            response = self.client.get(reverse(url_name_index))
            self.assertTrue(response.wsgi_request.user.is_authenticated)

        except Exception as e:
            print(f"❌ [ERROR EN {url_name_register.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{url_name_register}': {e}")

class ProfileReadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="nuevo_usuario", password="SuperSecreto123")

    def test_logout_redirects_to_app(self):
        template_exit = 'exit'
        try:
            self.client.login(username="nuevo_usuario", password="SuperSecreto123")
            response = self.client.get(reverse('exit'))

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('app'))

            response_index = self.client.get(reverse('profile'))
            self.assertEqual(response_index.status_code, 302)
            call_status(
                url_name=template_exit,
                response=response,
                expected_status=302,
                message="logout y redireccion hecho"
            )
        except Exception as e:
            print(f"❌ [ERROR EN {template_exit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_exit}': {e}")

    def test_read_profile(self):
        page_name = 'profile'

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        try:
            self.assertTrue(response.url.startswith('/accounts/login'))

            self.client.login(username="nuevo_usuario", password="SuperSecreto123")
            response = self.client.get(reverse(page_name))

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(template_use(page_name))

            expected_keys = ['label_username', 'label_first_name', 'label_last_name', 'label_email']
            for key in expected_keys:
                self.assertIn(key, response.context)
            call_status(
                url_name=page_name,
                response=response,
                expected_status=200,
                message="Vista de perfil cargada correctamente con los datos esperados"
            )
        except Exception as e:
            print(f"❌ [ERROR EN {page_name.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{page_name}': {e}")

class ProfileUpdataTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="nuevo_usuario", password="SuperSecreto123")
        self.other_user = User.objects.create_user(username="otro_usuario", password="OtraClave123")

    def test_edit_own_profile_succesfully(self):
        template_edit = "profile"

        self.client.login(username="nuevo_usuario", password="SuperSecreto123")
        url = reverse("profile_edit", kwargs={"pk": self.user.pk})

        try:
            data = {
                "username": "usuario_actualizado",
                "first_name": "Nuevo",
                "last_name": "Nombre",
                "email": "nuevo@email.com",
            }

            response = self.client.post(url, data, follow=True)  # usamos follow=True

            self.user.refresh_from_db()

            # Comprobamos que hubo redirección en algún punto
            self.assertGreater(len(response.redirect_chain), 0)
            self.assertEqual(response.status_code, 200)

            # Comprobamos datos actualizados
            self.assertEqual(self.user.username, "usuario_actualizado")
            self.assertEqual(self.user.email, "nuevo@email.com")

            # Comprobamos que se usó la plantilla correcta
            self.assertTemplateUsed(response, template_use(template_edit))

            # Validamos mensaje de éxito
            expected_msg = "Tu perfil se ha actualizado correctamente."
            messages = list(get_messages(response.wsgi_request))
            self.assertTrue(any(expected_msg in str(m) for m in messages))

            # Llamada a call_status con mensaje esperado
            call_status(
                response=response,
                url_name=template_edit,
                expected_status=200,
                message="usuario editado exitosamente",
                expected_message=expected_msg
            )

        except Exception as e:
            print(f"❌ [ERROR EN {template_edit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_edit}': {e}")
    
    def test_edit_profile_template_render(self):
        template_edit = "profile"

        self.client.login(username="nuevo_usuario", password="SuperSecreto123")
        url = reverse("profile_edit", kwargs={"pk": self.user.pk})

        try:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(template_use('profile_edit'))

            call_status(
                client=self.client,
                url_name=template_edit,
                expected_status=200,
                message="renderizado de la pagina exitoso"
            )

        except Exception as e:
            print(f"❌ [ERROR EN {template_edit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_edit}': {e}")

    def test_cannot_edit_other_user(self):
        template_edit = "profile"
        self.client.login(username="nuevo_usuario", password="SuperSecreto123")
        url = reverse("profile_edit", kwargs={"pk": self.other_user.pk})                

        try:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            call_status(
                response=response,
                url_name=template_edit,
                expected_status=404,
                message="No se puede editar otr usuario que no sea el tuyo"
            )

        except Exception as e:
            print(f"❌ [ERROR EN {template_edit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_edit}': {e}")

class ProfileDeleteTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(username="borrar_usuario", password="Clave123")

        def test_user_can_delete_own_account(self):
            template_delete =  "profile_delete"
            delete_url = reverse("profile_delete", kwargs={"pk": self.user.pk})
            success_url = reverse("app")

            self.client.login(username="borrar_usuario", password="Clave123")

            try:
                response_get = self.client.get(delete_url)
                self.assertEqual(response_get.status_code, 200)
                self.assertTemplateUsed(template_use('profile_delete'))

                response_post = self.client.post(delete_url, follow=True)

                self.assertRedirects(response_post, success_url)

                u_e = User.objects.filter(username="borrar_usuario").exists()

                self.assertFalse(u_e)

                self.assertFalse(response_post.wsgi_request.user.is_authenticated)

                call_status(
                    response=response_post,
                    url_name=template_delete,
                    expected_status=200,
                    message="usuario eliminado exitosamente"
                )                

            except Exception as e:
                print(f"❌ [ERROR EN {template_delete.upper()}] - {str(e)}")
                self.fail(f"Falló al testear la vista '{template_delete}': {e}")
