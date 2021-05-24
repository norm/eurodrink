from django.core.management.base import BaseCommand
import toml

from contests.models import (
    Language,
    Country,
    Contest,
)


class Command(BaseCommand):
    help = 'Import from eurovision_data/ files'

    def handle(self, *args, **options):
        self.load_countries('eurovision_data/countries.toml')
        self.load_contests('eurovision_data/contests.toml')

    def load_countries(self, data):
        countries = toml.load(data)
        for country in countries:
            langs = []
            for language in countries[country]['language']:
                lang, _ = Language.objects.get_or_create(id=language)
                langs.append(lang)
            del countries[country]['language']
            obj, _ = Country.objects.update_or_create(
                id=country,
                **countries[country],
            )
            for lang in langs:
                obj.languages.add(lang)

    def load_contests(self, data):
        contests = toml.load(data)
        for contest in contests:
            Contest.objects.update_or_create(
                year=contest,
                host=Country.objects.get(id=contests[contest]['host']),
            )
