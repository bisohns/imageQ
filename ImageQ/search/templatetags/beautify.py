from django import template

register = template.Library()

@register.filter
def add_class(form_input, css_class):
    """ Adds css class to a form field """
    return form_input.as_widget(attrs={'class': css_class})
