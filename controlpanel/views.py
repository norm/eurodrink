from datetime import date
from django.core.cache import cache
from django.views.generic import (
    CreateView,
    RedirectView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from contests.models import (
    Contest,
    Participant,
    Performance,
    Score,
)
from incidents.models import (
    PerformanceIncidentType,
    ShowIncidentType,
    ScoreIncidentType,
)


class PanelBase(LoginRequiredMixin):
    login_url = '/admin/login/'


class ControlPanel(PanelBase, TemplateView):
    template_name = 'controlpanel.html'

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
            context['reporting'] = cache.get('reporting')

            # to mark a participant as having participated in the scoring
            # round, they need to have given a performance a score (doesn't
            # matter which performance, as long as it is from this show)
            performance = Performance.objects.filter(show=show)[0]
            context['performance'] = performance

            voted = [
                x.country for x in
                    Score.objects.filter(performance=performance)
            ]
            remaining = [
                x for x in
                    Participant.objects.filter(contest=contest)
                        if x.country not in voted
            ]

            context['voted'] = sorted(
                voted,
                key=lambda c: c.english
            )
            context['remaining'] = sorted(
                remaining,
                key=lambda c: c.country.english
            )
            context['scoring_incidents'] = ScoreIncidentType.objects.all()
        return context


class SetScoringContext(PanelBase, RedirectView):
    url = '/panel/'

    def post(self, request, *args, **kwargs):
        participant = request.POST.get('participant')
        cache.set('reporting', Participant.objects.get(pk=participant), 600)
        return super().post(request, *args, **kwargs)


class ScoringComplete(PanelBase, CreateView):
    model = Score
    fields = ['points', 'country', 'performance', 'source']
    success_url = '/panel/'

    def post(self, request, *args, **kwargs):
        cache.delete('reporting')
        return super().post(request, *args, **kwargs)
