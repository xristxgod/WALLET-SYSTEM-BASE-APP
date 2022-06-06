from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(is_safe=True)
def set_widget(value: BoundField, data: str):
    """
    Set input basic widget
    :param value: ...
    :param data: Example: class="form-control form-control-lg",type="text"
    """
    attrs = {}
    for d in data.split(","):
        key, val = d.split("=")
        attrs.update({
            key: val.replace(val[0], "")
        })
    value.field.widget.attrs.update(**attrs)
    return value





