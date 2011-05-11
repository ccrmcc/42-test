from django.forms import widgets


class JqueryDate(widgets.TextInput):
    CLASS_NAME = 'jquery-date'

    def __init__(self, attrs=None, *a, **kw):

        if not isinstance(attrs, dict):
            attrs = {}

        attrs['class'] = 'jquery-date'

        super(JqueryDate, self).__init__(attrs=attrs, *a, **kw)
