from django.template.base import Library
from django.template.base import Node
from django.template.base import TemplateSyntaxError, VariableDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = Library()

class AdminLinkNode(Node):
    def __init__(self, var):
        self.var = var
    def render(self, context):
        try:
            obj = self.var.resolve(context, True)
        except VariableDoesNotExist:
            return ''

        url = reverse('admin:%s_%s_change' %(
            obj._meta.app_label,  obj._meta.module_name),
            args=[obj.id]
        )

        return mark_safe('<a href="%s">edit %s in admin</a>' % (url, obj))

@register.tag
def edit_link(parser, token):
    try:
        tag, var = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError( "edit_link tag requires a single argument")
    return AdminLinkNode(parser.compile_filter(var))

