from django.contrib import admin

from .models import (
    Language,
    Country,
    Contest,
)

admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Contest)
