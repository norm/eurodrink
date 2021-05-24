from django.contrib import admin

from .models import (
    Language,
    Country,
    Contest,
    Singer,
    Artist,
    Song,
    Participant,
)

admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Contest)
admin.site.register(Singer)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Participant)
