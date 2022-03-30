# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from scout_manager.dao.groups import update_groups


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_groups()
