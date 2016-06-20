from django.core.management.base import BaseCommand, CommandError
from scout_manager.dao.groups import update_groups

class Command(BaseCommand):

    def handle(self, *args, **options):
        update_groups()


