from django import template

register = template.Library()


@register.inclusion_tag('components/auth/form.html')
def render_form(form, titulo, contents, content_button, name=None):
    """
    Inclusion tag para renderizar un formulario reutilizable.
    - form: instancia de un formulario
    - titulo: título del formulario
    - contents: lista de campos a mostrar
    - content_botton: texto del botón
    - name: para el atributo name
    """
    # Si 'contents' viene como string separado por comas, conviértelo en lista
    if isinstance(contents, str):
        contents = [campo.strip() for campo in contents.split(',')]

    campos = {field: form[field] for field in contents}

    context = {
        'form': form,
        'titulo': titulo,
        'contents': campos,
        'content_button': content_button,
        'name': name
    }

    return context