from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from contests.models import Show
from incidents.models import (
    PerformanceIncidentType,
    ShowIncidentType,
    ScoreIncidentType,
)


class ControlPanel(LoginRequiredMixin, TemplateView):
    template_name = 'controlpanel.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # FIXME hardcoded
        show = Show.objects.get(id='2021-final')
        context['show'] = show
        context['performance_incidents'] = PerformanceIncidentType.objects.all()
        context['show_incidents'] = ShowIncidentType.objects.all()
        context['score_incidents'] = ScoreIncidentType.objects.all()
        return context
