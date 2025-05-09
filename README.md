TurtleGlide
================

**Introducción**
---------------

TurtleGlide es una herramienta para crear archivos dentro de la carpeta `templates` o `static` de una app de Django.

**Instalación del paquete**
-------------------------

### Instalación en tu proyecto Django

Instalar TurtleGlide en tu proyecto Django:

```bash
pip install TurtleGlide
```

Luego, agregar TurtleGlide como una app de Django en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'TurtleGlide'
]
```

**Uso de TurtleGlide**
---------------------

### Parámetros obligatorios

Hay tres parámetros obligatorios para el uso del comando `create_archive`:

* `app_name`: Nombre de la app
* `file_path`: Ruta del componente HTML
* `--template` para archivos en la carpeta `templates`
* `--static` para archivos en la carpeta `static`

### Comando de ejemplo

```bash
python manage.py create_archive "app_name" --static "file_path"
```

**Otras funciones el uso de commandos**
---------------------

| Función | Descripción | Código de ejemplo |
| --- | --- | --- |
| [create_archive](#funciones) | Crea archivos en las carpetas `static` y `templates` | [Ver ejemplo](#create-archive) |

**Funciones**
---------------------

### create_archive

Crea multiples archivos en las carpetas `static` y `templates` de una app de Django.

```bash
python manage.py create_archive home --static css/app.css --template layouts/main.html
```

>[!NOTE]
>La carpeta llamada "chocolate" contiene un proyecto de Django utilizado para realizar pruebas y analizar nuevas implementaciones.


**Instalación para desarrolladores**
---------------------------------

### Paso 1: Instalar dependencias y crear entorno virtual

Llamar al script `setup.sh` para instalar las dependencias y crear el entorno virtual:

```bash
./setup.sh
```

### Paso 2: Activar entorno virtual

Activar el entorno virtual:

```bash
source venv/bin/activate
```

### Listo para empezar

Ya estás listo para empezar a trabajar con TurtleGlide sin problemas.

### cosas por hacer
1. CRUD y contraseña
   - [ ] hacer los test para el CRUD y la contraseña
   - [ ] hacer mas complejo y mas robusto el test de test_password_confirm
2. estilos
   - [ ] terminar los estilos
3. svg
	- [ ] encontrar un svg para el navbar y la portada
4. traducción
   - [ ] mejorar las salidas de texto para diferentes idiomas 
