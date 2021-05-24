from datetime import date
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from contests.models import (
    Contest,
    Performance,
)
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
        contest = Contest.objects.get(year=date.today().year)
        show = contest.show_set.get(type='final')
        context['show'] = show
        context['performance_incidents'] = PerformanceIncidentType.objects.all()
        context['show_incidents'] = ShowIncidentType.objects.all()
        context['score_incidents'] = ScoreIncidentType.objects.all()

        performances = Performance.objects.filter(
            show=show,
            occurred=False,
        )
        if performances.count() > 0:
            context['mode'] = 'performance'
            context['this'] = performances[0]
            context['all'] = performances
        else:
            context['mode'] = 'scoring'
        return context
