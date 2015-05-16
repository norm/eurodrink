from django.db import models

AMOUNTS=(
    (1, 'One finger'),
    (2, 'Two fingers'),
    (3, 'Down your drink'),
)
STAGES=(
    (1, 'During the performance'),
    (2, 'During the scoring'),
)

class Incident(models.Model):
    status = models.CharField(max_length=140)
    button = models.CharField(max_length=40)
    description = models.CharField(max_length=256)
    stage = models.IntegerField(choices=STAGES, default=1)
    amount = models.IntegerField(choices=AMOUNTS, default=1)

    @classmethod
    def performance_incidents(kls):
        return kls.objects.filter(stage=1)

    @classmethod
    def scoring_incidents(kls):
        return kls.objects.filter(stage=2)

    def amount_class(self):
        """ The CSS class for this amount """
        if self.amount == 1:
            return 'one'
        elif self.amount == 2:
            return 'two'
        elif self.amount == 3:
            return 'down'
        return ''

    def __unicode__(self):
        return self.button

    class Meta:
        ordering = ['button']
