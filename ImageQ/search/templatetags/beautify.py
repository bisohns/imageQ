from django import template

register = template.Library()

@register.filter
def add_class(form_input, css_class):
    """ Adds css class to a form field """
    return form_input.as_widget(attrs={'class': css_class})

@register.filter
def add_attribute(form_input, attribute):
    """ Adds attribute to a form field """
    return form_input.as_widget(attrs={str(attribute): "environment"})

@register.filter
def get_href(search_results, index):
    """ gets href for search results """
    return search_results["links"][index]

@register.filter
def get_index(predictions, new_index):
    """get index from predictions"""
    return predictions[new_index]["index"]

@register.simple_tag
def get_item(dictionary, key, index):
    """ loads the dictionary value and specified index """
    item = dictionary.get(key)
    return item[index]

@register.simple_tag
def get_pred_item(list_, index, key):
    """ retrieves value of key from dicts in a list"""
    dict_ = list_[index]
    return dict_.get(key)
