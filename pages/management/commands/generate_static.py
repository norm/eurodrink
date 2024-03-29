from django.core.management.base import BaseCommand

from pages.pages import HomePage, RecipePage


class Command(BaseCommand):
    help = 'Generates eurovisiondrinking.com'

    def handle(self, *args, **options):
        HomePage().generate()
        RecipePage().generate()
