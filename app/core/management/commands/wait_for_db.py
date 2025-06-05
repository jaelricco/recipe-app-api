"""
Django command to wait for the database to be available.
"""
import time  # to make execution sleep

from psycopg2 import OperationalError as Psycopg2OpError  # Error Psycopg2 package throws when databse is not ready -> rames the OperationalError to Psycopg2OpError

from django.db.utils import OperationalError  # Error Django throws when database is not ready
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])  # checks if database is ready -> if not ready is raises a exception -> line 23!
                db_up = True
            except(Psycopg2OpError, OperationalError):  # when getting Psycopg2 or Operational Error -> write short msg and wait for 1 sec
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
