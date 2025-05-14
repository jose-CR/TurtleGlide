turtle_glide
================

**Introducción**
---------------

turtle_glide es una herramienta para crear archivos dentro de la carpeta `templates` o `static` de una app de Django.

**Instalación del paquete**
-------------------------

### Instalación en tu proyecto Django

Instalar turtle_glide en tu proyecto Django:

```bash
pip install turtle_glide
```

Luego, agregar TurtleGlide como una app de Django en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'turtle_glide'
]
```

**Uso de turtle_glide**
---------------------

### Parámetros obligatorios

Hay tres parámetros obligatorios para el uso del comando `create_archive`:

* `app_name`: Nombre de la app
* `file_path`: Ruta del componente
* `--type`: Tipo de archivo a crear:
	+ `template` para archivos en la carpeta `templates`
	+ `static` para archivos en la carpeta `static`

### Comando de ejemplo
```bash
python manage.py create_archive "app_name" "file_path" --type="template"
```

**uso de turtle_glide para desarrolladores**
------------

hay tres paramentros obligatorios para el uso del comando creeate_archive:

### Paso 1: Instalar dependencias y crear entorno virtual

comandos:
-----------

#### instalacion de dependencias

```bash
./setup.sh
```

### Paso 2: Activar entorno virtual
Activar el entorno virtual:

```bash
source venv/bin/activate
```

#### variables

- app_name: Nombre de la app
- file_path: Ruta del componente
- --type: de forma determinada el tipo de archivo a crear: "template" para archivos en la carpeta templates, "static" para archivos en la carpeta static

```bash
python manage.py create_archive "app_name" "file_path" --type="template"
```

### Listo para empezar
Ya estás listo para empezar a trabajar con TurtleGlide sin problemas.