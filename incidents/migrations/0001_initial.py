# Generated by Django 3.1.7 on 2021-05-24 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0007_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseIncidentType',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=230)),
                ('tweet', models.CharField(blank=True, max_length=230, null=True)),
                ('penalty', models.CharField(choices=[('one-finger', 'One finger'), ('two-fingers', 'Two fingers'), ('down', 'Down your drink')], max_length=12)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ShowIncident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.show')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreIncident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.participant')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceIncident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.performance')),
            ],
        ),
        migrations.CreateModel(
            name='ShowIncidentType',
            fields=[
                ('baseincidenttype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='incidents.baseincidenttype')),
                ('show', models.ManyToManyField(blank=True, through='incidents.ShowIncident', to='contests.Show')),
            ],
            bases=('incidents.baseincidenttype',),
        ),
        migrations.AddField(
            model_name='showincident',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.showincidenttype'),
        ),
        migrations.CreateModel(
            name='ScoreIncidentType',
            fields=[
                ('baseincidenttype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='incidents.baseincidenttype')),
                ('participant', models.ManyToManyField(blank=True, through='incidents.ScoreIncident', to='contests.Participant')),
            ],
            bases=('incidents.baseincidenttype',),
        ),
        migrations.AddField(
            model_name='scoreincident',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.scoreincidenttype'),
        ),
        migrations.CreateModel(
            name='PerformanceIncidentType',
            fields=[
                ('baseincidenttype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='incidents.baseincidenttype')),
                ('performances', models.ManyToManyField(blank=True, through='incidents.PerformanceIncident', to='contests.Performance')),
            ],
            bases=('incidents.baseincidenttype',),
        ),
        migrations.AddField(
            model_name='performanceincident',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.performanceincidenttype'),
        ),
    ]
