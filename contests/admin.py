from django.contrib import admin

from .models import (
    Language,
    Country,
    Contest,
    Singer,
    Artist,
    Song,
    Participant,
    Show,
    Performance,
)

admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Contest)
admin.site.register(Singer)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Participant)
admin.site.register(Show)
admin.site.register(Performance)
