"""
Mixins for shared behaviors between scripts
"""
from datetime import datetime, timedelta
from server.utils.arx_utils import time_now


class RunDateMixin(object):
    """Mixin for checking remaining time"""
    @property
    def time_remaining(self):
        """
        Returns the time the update is scheduled to run.AccountTransaction

            Returns:
                remaining (Timedelta): remaining time before weekly update will process
        """
        # self.db.run_date is the date we're scheduled to run the weekly update on
        remaining = self.db.run_date - time_now(aware=True)
        return remaining

    def check_event(self):
        """
        Determine if enough time has passed. Return true if so.

            Returns:
                bool: whether we're ready for weekly event to run or not
        """
        rounding_check = timedelta(minutes=5)
        if self.time_remaining < rounding_check:
            return True
        else:
            return False
