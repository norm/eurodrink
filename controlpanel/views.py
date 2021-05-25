from datetime import date
from django.core.cache import cache
from django.views.generic import (
    CreateView,
    RedirectView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import tweepy

from contests.models import (
    Contest,
    Participant,
    Performance,
    Score,
)
from incidents.models import (
    PerformanceIncidentType,
    PerformanceIncident,
    ShowIncidentType,
    ScoreIncidentType,
    ScoreIncident,
)


class PanelBase(LoginRequiredMixin):
    login_url = '/admin/login/'

    def send_tweet(self, text):
        auth = tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
        )
        auth.set_access_token(
            os.environ['ACCESS_TOKEN'],
            os.environ['ACCESS_TOKEN_SECRET'],
        )
        api = tweepy.API(auth)
        api.update_status(text)


class ControlPanel(PanelBase, TemplateView):
    template_name = 'controlpanel.html'

    def get_twitter_account(self):
        account = cache.get('twitter_account')
        if not account:
            auth = tweepy.OAuthHandler(
                os.environ['CONSUMER_KEY'],
                os.environ['CONSUMER_SECRET'],
            )
            auth.set_access_token(
                os.environ['ACCESS_TOKEN'],
                os.environ['ACCESS_TOKEN_SECRET'],
            )
            api = tweepy.API(auth)
            tweeter = api.verify_credentials()
            cache.set('twitter_account', tweeter.screen_name, 3600)
            account = cache.get('twitter_account')
        return account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contest = Contest.objects.get(year=date.today().year)
        show = contest.show_set.get(type='final')
        context['show'] = show
        context['show_incidents'] = ShowIncidentType.objects.all()
        context['score_incidents'] = ScoreIncidentType.objects.all()
        context['twitter_account'] = self.get_twitter_account()

        performances = Performance.objects.filter(
            show=show,
            occurred=False,
        )
        if performances.count() > 0:
            context['mode'] = 'performance'
            context['this'] = performances[0]
            context['all'] = performances
            context['happened_incidents'] = PerformanceIncident.objects.filter(
                performance=performances[0],
                predicted=False,
            )
            context['draft_incidents'] = PerformanceIncident.objects.filter(
                performance=performances[0],
                predicted=True,
            )
            possible_incidents = []
            for incident_type in PerformanceIncidentType.objects.all():
                append = 1
                for incident in context['happened_incidents']:
                    if incident.type == incident_type:
                        append = 0
                for incident in context['draft_incidents']:
                    if incident.type == incident_type:
                        append = 0
                if append:
                    possible_incidents.append(incident_type)
            context['possible_incidents'] = possible_incidents

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
            context['happened_incidents'] = ScoreIncident.objects.filter(
                participant=context['reporting']
            )
            possible_incidents = []
            for incident_type in ScoreIncidentType.objects.all():
                append = 1
                for incident in context['happened_incidents']:
                    if incident.type == incident_type:
                        append = 0
                if append:
                    possible_incidents.append(incident_type)
            context['possible_incidents'] = possible_incidents
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


class FreeTweet(PanelBase, RedirectView):
    url = '/panel/'

    def post(self, request, *args, **kwargs):
        tweet = request.POST.get('tweet')
        self.send_tweet('%s #Eurovision #esc%d' % (tweet, date.today().year))
        return super().post(request, *args, **kwargs)
