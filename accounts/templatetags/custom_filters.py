from django import template

register = template.Library()


@register.filter
def add_classes(field, css_classes):
    return field.as_widget(attrs={"class": css_classes})


@register.filter
def input_type(field):
    return field.field.widget.__class__.__name__
