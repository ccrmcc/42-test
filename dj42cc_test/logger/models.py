from django.db import models
from picklefield import PickledObjectField


class HttpLogEntry(models.Model):
    data = PickledObjectField()
    add_datetime = models.DateTimeField(auto_now_add=True)

