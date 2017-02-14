from django.core.management.base import BaseCommand, CommandError
from cut_link.models import CutURL


class Command(BaseCommand):
    help = 'Refresh all short links'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
        return CutURL.objects.refresh(items=options['items'])

    # ./manage.py refresh --items 2    <-- example
    # look at refresh function at models file!
