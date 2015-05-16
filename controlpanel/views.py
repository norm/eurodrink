from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View

from .models import Context
from incidents.models import Incident
from twitter_accounts.models import Account


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ControlPanelView(LoginRequiredMixin, TemplateView):
    template_name = 'controlpanel.html'

    def get_context_data(self, **kwargs):
        context = super(ControlPanelView, self).get_context_data(**kwargs)

        context['current_context'] = Context.current()

        account = Account.active_account()
        context['current_account'] = account
        context['recent_tweets'] = account.recent_tweets()

        context['performance_incidents'] = Incident.performance_incidents()
        context['scoring_incidents'] = Incident.scoring_incidents()

        return context


class ContextView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        context = Context.current()
        context.text = request.POST.get('context', '')
        context.save()
        return HttpResponseRedirect('/panel/')


class TweetView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = request.POST.get('tweet', None)
        if tweet:
            account = Account.active_account()
            account.tweet_with_context(tweet)
        return HttpResponseRedirect('/panel/')
