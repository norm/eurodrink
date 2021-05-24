from .models import StaticPage

from incidents.models import (
    PerformanceIncidentType,
    ShowIncidentType,
    ScoreIncidentType,
)


class HomePage(StaticPage):
    template_name = 'homepage.html'

    def get_context(self):
        return {
            'performance_incidents': PerformanceIncidentType.objects.all(),
            'show_incidents': ShowIncidentType.objects.all(),
            'scoring_incidents': ScoreIncidentType.objects.all(),
        }
