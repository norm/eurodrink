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

        context['performance_incidents'] = Incident.performance_incidents()
        context['scoring_incidents'] = Incident.scoring_incidents()

        return context
