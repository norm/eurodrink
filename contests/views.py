from django.views.generic.edit import UpdateView

from .models import Performance


class PerformanceUpdate(UpdateView):
    model = Performance
    fields = ['occurred']
    success_url = '/panel/'
