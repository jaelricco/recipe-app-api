"""
Test custom Django management commands.
"""
from unittest.mock import patch  # to mock behaviour -> to simulate if database is returning a response or not

from psycopg2 import OperationalError as Psycopg2Error  # Error exception that might be thrown -> want to catch

from django.core.management import call_command  # helper function from django to call a command by a name
from django.db.utils import OperationalError  # Error exception that might be thrown -> want to catch
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')  # mocking the check method -> core/management/commands/wait_for_db.py -> Command function -> check method
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):  # parameters are getting added from the inside out
        """Test waiting for database when getting OperationalError."""

        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        # first 2 times raises a Psycopg2Error, the next 3 times a OperationalError, the sixth time we call it it returns True

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
