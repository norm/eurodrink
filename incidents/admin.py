from django.contrib import admin

from .models import (
    PerformanceIncidentType,
    PerformanceIncident,
    ScoreIncidentType,
    ScoreIncident,
    ShowIncidentType,
    ShowIncident,
)

admin.site.register(PerformanceIncidentType)
admin.site.register(PerformanceIncident)
admin.site.register(ScoreIncidentType)
admin.site.register(ScoreIncident)
admin.site.register(ShowIncidentType)
admin.site.register(ShowIncident)
