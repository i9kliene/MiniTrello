from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Board)
admin.site.register(models.Section)
admin.site.register(models.Tag)
admin.site.register(models.Card)
