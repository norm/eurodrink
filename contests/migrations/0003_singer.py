# Generated by Django 3.1.7 on 2021-05-24 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_contest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('known_as', models.CharField(max_length=128)),
                ('born', models.DateField(blank=True, null=True)),
                ('died', models.DateField(blank=True, null=True)),
                ('citizenship', models.ManyToManyField(to='contests.Country')),
            ],
        ),
    ]