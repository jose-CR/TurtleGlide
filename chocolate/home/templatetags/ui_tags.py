from django import template

register = template.Library()

@register.inclusion_tag('components/ui/button.html')
def button(title_button, href=None, parent_class=None, btn_class='', align='center', size='md', color='primary', text_color='white'):
    """
    Renderiza un botón reutilizable con varias opciones de estilo.

    Args:
    - title_button (str): Texto dentro del botón.
    - href (str): Si se proporciona, se usa un <a>, si no, <button>.
    - parent_class (str): Clase personalizada para el contenedor padre.
    - btn_class (str): Clases extra para el botón.
    - align (str): Alineación del botón (left, center, right). Default: center.
    - size (str): Tamaño del botón (sm, md, lg). Default: sm.
    - color (str): Color del fondo. Puede ser clase ('primary') o código hexadecimal ('#ff0000').
    - text_color (str): Color del texto. Igual que color.
    """
    return {
        'title_button': title_button,
        'href': href,
        'parent_class': parent_class,
        'btn_class': btn_class,
        'align': align,
        'size': size,
        'color': color,
        'text_color': text_color,
    }