from django import template

register = template.Library()

@register.filter
def add_class(form_input, css_class):
    """ Adds css class to a form field """
    return form_input.as_widget(attrs={'class': css_class})

@register.filter
def get_href(search_results, index):
    """ gets href for search results """
    return search_results["links"][index]

@register.simple_tag
def get_item(dictionary, key, index):
    """ loads the dictionary value and specified index """
    item = dictionary.get(key)
    return item[index]
