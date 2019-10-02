#!/usr/bin/env python3
import unittest
from log_consumer import Logger
from datetime import date

test_type = 'TEST'
test_message = 'This is a test message.'



class TestLogger(unittest.TestCase):
    """
    Test Logger class methods.
    """

    def test_get_log_filename(self):
        """
        Test `get_log_filename` gets a path with the date.
        """
        filename = Logger('/tmp').get_log_filename()
        self.assertEqual(filename, '/tmp/' + str(date.today()) + '.log')


    def test_format_message(self):
        """
        Test `format_message` formats message correctly.
        """
        logger = Logger('/tmp')
        message = logger.format_message(test_type, test_message)

        self.assertTrue(message.startswith(f'[{date.today()}'))
        self.assertTrue(message.endswith(f'{test_type}: {test_message}\n'))


    def test_write_log(self):
        """
        Test that `write_log`...
            * Creates a log file if none exist.
            * Writes to an accessible path
        """
        logger = Logger('/tmp')
        logger.write_log(test_type, test_message)

        with open(logger.get_log_filename(), 'r') as f:
            output = f.read()

        self.assertTrue(output.endswith(f'{test_message}\n'))
