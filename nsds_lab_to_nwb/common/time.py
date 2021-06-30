import logging.config
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LOCAL_TIMEZONE = pytz.timezone('US/Pacific')


def get_current_time(timezone=LOCAL_TIMEZONE):
    current_time = datetime.now(tz=pytz.utc).astimezone(timezone)
    return current_time


def get_default_time(timestamp=0, timezone=LOCAL_TIMEZONE):
    # just return a dummy datetime object
    return datetime.fromtimestamp(timestamp, tz=timezone)


def validate_time(time_object, timezone=LOCAL_TIMEZONE):
    if not isinstance(time_object, datetime):
        raise TypeError('should be a datetime object.')
    return time_object.astimezone(timezone)
