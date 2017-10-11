from django.core.management.base import BaseCommand, CommandError
from core import views


class Command(BaseCommand):
    help = 'Get all repositories'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        try:
            print('Getting all repositories from: ' + options['username'])
            print(views.getRepositories(options['username']))
        except Exception as e:
            raise CommandError(repr(e))
