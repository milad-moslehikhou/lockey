from django import template

register = template.Library()


@register.inclusion_tag('partials/components/text_input.html')
def mdl_text_input(field):
    return {'field': field}


@register.inclusion_tag('partials/components/password_input.html')
def mdl_password_input(field):
    return {'field': field}


@register.inclusion_tag('partials/components/primary_button.html')
def mdl_primary_button(type, label):
    return {'type': type, 'label': label}


@register.simple_tag(takes_context=True)
def set_breakpoint(context, *args):
    breakpoint()
