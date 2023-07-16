from django.template.loader import render_to_string
from django import template
import platform

register = template.Library()


@register.filter
def add_classes(field, css_classes):
    return field.as_widget(attrs={"class": css_classes})


@register.filter
def input_type(field):
    return field.field.widget.__class__.__name__

@register.filter
def os_path(field):
    """
    Returns the right file path according to OS
    """
    operating_system = platform.uname().system
    if operating_system == "Windows":
        if "/" in field:
            new_path = field.split('/')
            new_path = "\\".join(new_path)
            return new_path
        return field
    else:
        if "\\" in field:
            new_path = field.split('\\')
            new_path = "/".join(new_path)
            return new_path
        return field
    
@register.simple_tag
def custom_include(template_name):
    """
    This function is to handle template inclusion
    Not yet completed
    """
    operating_system = platform.uname().system
    new_path = template_name
    if operating_system == "Windows":
        if "/" in template_name:
            new_path = template_name.split('/')
            new_path = "\\".join(new_path)
    else:
        if "\\" in template_name:
            new_path = template_name.split('\\')
            new_path = "/".join(new_path)
    rendered_template = render_to_string(new_path)
    return rendered_template