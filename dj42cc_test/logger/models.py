from django.db import models
from picklefield import PickledObjectField
from django.db.models.signals import post_save, post_delete


class HttpLogEntry(models.Model):
    data = PickledObjectField()
    add_datetime = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)


class ModelLogEntry(models.Model):
    ACTIONS = (
            ("edit", "Edited"),
            ("create", "Created"),
            ("delete", "Deleted"),
    )
    model_name = models.CharField(max_length=50)
    action = models.CharField(choices=ACTIONS, max_length=50)
    changed_pk = models.IntegerField()  # cant use foreign key
    datetime = models.DateTimeField(auto_now_add=True)

    @classmethod
    def log(cls, action, instance):
        # dont log self
        if isinstance(instance, cls):
            return

        name = '%s.%s' % (instance._meta.app_label, instance._meta.module_name)
        pk = instance.pk if isinstance(instance.pk, (int, long)) else 0
        log = cls(model_name=name, action=action, changed_pk=pk)
        log.save()

log = ModelLogEntry.log


def save_handler(instance, created, **kw):
    action = 'create' if created else 'edit'
    log(action, instance)


def delete_handler(instance, **kw):
    log("delete", instance)


post_save.connect(save_handler)
post_delete.connect(delete_handler)
