from django.views.generic.edit import CreateView

from .models import PerformanceIncident, ScoreIncident, ShowIncident


class PerformanceIncidentCreate(CreateView):
    model = PerformanceIncident
    fields = ['type', 'performance']
    success_url = '/panel/'


class ScoreIncidentCreate(CreateView):
    model = ScoreIncident
    fields = ['type', 'participant']
    success_url = '/panel/'


class ShowIncidentCreate(CreateView):
    model = ShowIncident
    fields = ['type', 'show']
    success_url = '/panel/'
