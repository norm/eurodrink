from django.views.generic import TemplateView

from incidents.models import Incident


class HomepageView(TemplateView):
    model = Incident
    template_name = 'homepage.html'
    context_object_name = 'incidents'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['performance_incidents'] = Incident.performance_incidents()
        context['scoring_incidents'] = Incident.scoring_incidents()
        return context
