from django.contrib import admin

from .models import (
    Language,
    Country,
    Contest,
    Singer,
)

admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Contest)
admin.site.register(Singer)
