from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Model
from django.utils.importlib import import_module


class Command(BaseCommand):
    args = ""
    help = "Counts all registered models"

    def out(self, msg):
        self.stdout.write("%s\n" % msg)
        self.stderr.write("error: %s\n" % msg)

    def handle(self, *args, **kw):

        for app in settings.INSTALLED_APPS:
            models = import_module("%s.models" % app)

            self.inspect_models(models)

    def inspect_models(self, models):
        for obj_name in dir(models):
            obj = getattr(models, obj_name)

            try:
                if issubclass(obj, Model):
                    self.count_model(obj)
            except TypeError:
                pass

    def count_model(self, model):
        count = model.objects.count()
        self.out("found model %r, count %d" % (model, count))
