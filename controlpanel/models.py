from django.db import models


class Context(models.Model):
    text = models.CharField(max_length=40)

    @classmethod
    def current(kls):
        return kls.objects.filter(pk=1)[0]

    def __unicode__(self):
        return 'Current Context'
