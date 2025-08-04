# 🐢 Turtle Glide

## 🧭 Introducción

**Turtle Glide** es una herramienta diseñada para **acelerar tareas comunes en proyectos Django**, como la creación de estructuras de autenticación y archivos base (`static`, `templates`). Ideal para desarrolladores que buscan ahorrar tiempo y seguir buenas prácticas.

---

## 🚀 Instalación

### 1. Instalar el paquete

```bash
pip install turtle_glide
```

### 2. Agregar a `INSTALLED_APPS`

En tu archivo `settings.py`, agrega:

```python
INSTALLED_APPS = [
    ...
    'turtle_glide',
]
```

---

## 📦 Funcionalidades

### ✅ Comandos disponibles

#### 1. `create_archive`

Crea archivos dentro de las carpetas `static/` y `templates/` de una app Django.

**Parámetros:**

* `app_name`: nombre de la app.
* `--template`: lista de archivos que irán en `templates/`.
* `--static`: lista de archivos que irán en `static/`.

**Ejemplo de uso:**

```bash
python manage.py create_archive home --static css/app.css js/app.js --template layouts/main.html
```

---

#### 2. `create_app`

Genera automáticamente una estructura de app llamada `home`, con todo lo necesario para:

* Autenticación de usuarios
* Registro
* Perfil
* Cambio/restablecimiento de contraseña
* Soporte multilenguaje
* Plantillas modulares (cards, botones, formularios reutilizables)
* Envío de correos

**Uso:**

```bash
python manage.py create_app
```

---

## 🛠️ Uso para desarrolladores

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tuusuario/turtle_glide.git
   cd turtle_glide
   ```

2. Ejecuta el script de instalación:

   ```bash
   bash setup.sh
   ```

3. Activa el entorno virtual:

   ```bash
   source venv/bin/activate
   ```

---

## 🌍 Traducción

La app `home` ya está preparada para múltiples idiomas usando `gettext`.
Para habilitar traducciones:

1. Crea la carpeta `locale/` dentro de `home/`.

2. Ejecuta:

```bash
python manage.py makemessages -l es
python manage.py compilemessages
```

3. Asegúrate de incluir en `settings.py`:

```python
LANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_L10N = True
USE_ACCEPT_LANGUAGE_HEADER = False
```

---

## 🧪 Tests

Turtle Glide incluye pruebas para:

* Registro y login
* Edición/eliminación de perfil
* Cambio y recuperación de contraseña

Para ejecutarlas:

```bash
python manage.py test home
```

---

## 🔧 Cosas por mejorar

1. Aplicar más principios **DRY** y **KISS**
2. Mejorar la interfaz de usuario (UI)
3. Incorporar peticiones **AJAX** para mejor UX
4. Optimizar la interfaz para **dispositivos móviles**

---

## 🤝 Contribuciones

¿Quieres contribuir o reportar un bug?
Abre un [issue](https://github.com/tuusuario/turtle_glide/issues) o un pull request. ¡Toda ayuda es bienvenida!

---
