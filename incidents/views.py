from django.views.generic.edit import CreateView, UpdateView

from .models import PerformanceIncident, ScoreIncident, ShowIncident


class PerformanceIncidentUpdate(UpdateView):
    model = PerformanceIncident
    fields = ['predicted']
    success_url = '/panel/'


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
