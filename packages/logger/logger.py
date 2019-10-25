#!/usr/bin/env python3
import os
import os.path
from datetime import datetime, date



class Logger:
    """
    Logging system.
    """

    def __init__(self, path: str):
        """
        Set path and create path directory if non-existant.
        """
        self.path = path

        # Create path
        if not os.path.exists(path):
            os.mkdir(path)

        # Ensure access to log path
        if not os.access(path, os.W_OK):
            raise PermissionError()


    def get_log_filename(self):
        """
        Get the file name of the log file.
        This method does not create the log file.
        """
        return os.path.join(self.path, str(date.today()) + '.log')


    def format_message(self, message_type: str, message: str):
        """
        Create formatted message based on message type and content.
        """
        return f'[{datetime.now()}] {message_type}: {message}\n'


    def write_log(self, message_type: str, message: str):
        """
        Write message to log file.
        """
        if message_type is None or message is None:
            return

        with open(self.get_log_filename(), 'a+') as f:
            f.write(self.format_message(message_type, message))
