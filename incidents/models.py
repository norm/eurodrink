from django.db import models

AMOUNTS=(
    (1, 'One finger'),
    (2, 'Two fingers'),
    (3, 'Down your drink'),
)

class Incident(models.Model):
    status = models.CharField(max_length=140)
    button = models.CharField(max_length=40)
    description = models.CharField(max_length=256)
    amount = models.IntegerField(choices=AMOUNTS)

    def __unicode__(self):
        return self.button
