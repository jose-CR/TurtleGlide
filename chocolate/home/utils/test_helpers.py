from django.urls import reverse
from django.contrib.messages import get_messages

def template_use(name):
    templates = {
        'app': 'index.html',
        # CRUD profile 
        'register': 'registration/register.html',
        'profile': 'profile.html',
        'profile_edit': 'profile/profile-edit.html',
        'profile_delete': 'profile/profile-delete.html'
        # Password
    }
    return templates.get(name)

def call_status(response=None, *, client=None, url_name=None, expected_status=200, message="", expected_message=None, method="get", data=None):
    if response is None:
        if not client or not url_name:
            raise ValueError("Si no se pasa 'response', se deben pasar 'client' y 'url_name'.")
        
        url = reverse(url_name)
        method = method.lower()
        
        if method == "post":
            response = client.post(url, data or {})
        else:
            response = client.get(url)

    if expected_message:
        messages = list(get_messages(response.wsgi_request))
        if any(expected_message in str(m) for m in messages):
            print(f"✅ [{url_name.upper()}] MENSAJE OK → '{expected_message}'")
        else:
            print(f"❌ [{url_name.upper()}] MENSAJE NO ENCONTRADO → '{expected_message}'")

    if response.status_code == expected_status:
        print(f"✅ [{url_name.upper() if url_name else ''}] PASÓ ({expected_status}) → {message}")
    else:
        print(f"❌ [{url_name.upper() if url_name else ''}] FALLÓ - Esperado: {expected_status}, Recibido: {response.status_code} → {message}")

    return response

