import logging.config
from datetime import datetime
import pytz

from nsds_lab_to_nwb.components.tdt.tdt_reader import TDTReader


logger = logging.getLogger(__name__)

LOCAL_TIMEZONE = pytz.timezone('US/Pacific')
_DEFAULT_SESSION_START_TIME = datetime.fromtimestamp(0, tz=LOCAL_TIMEZONE)


class SessionTimeExtractor():
    def __init__(self, dataset, metadata):
        self.dataset = dataset
        self.metadata = metadata

    @staticmethod
    def get_current_time(timezone=None):
        timezone = timezone or LOCAL_TIMEZONE
        current_time = datetime.now(tz=pytz.utc).astimezone(timezone)
        return current_time

    def get_session_start_time(self):
        if self.metadata.get('session_start_time', None) is not None:
            logger.info('Extracting session_start_time from metadata input...')
            return self._validate_time(self.metadata['session_start_time'])

        # if not found in metadata, try to extract from neural data recording
        try:
            logger.info('Extracting session_start_time from TDT...')
            session_start_time = self.extract_tdt_start_time(self.dataset.tdt_path)
            return self._validate_time(session_start_time)
        except AttributeError:
            logger.info('Could not extract from TDT. Using a default session_start_time.')
            return _DEFAULT_SESSION_START_TIME

    @staticmethod
    def extract_tdt_start_time(tdt_path, timezone=None):
        timezone = timezone or LOCAL_TIMEZONE
        tdt_reader = TDTReader(tdt_path)
        tdt_info = tdt_reader.tdt_obj['info']
        start_date = tdt_info['start_date'] # datetime object without timezone info
        # TODO: check timezone of the start_date recorded in tdt!
        session_start_time = start_date.astimezone(timezone)
        return session_start_time

    def _validate_time(self, time_object):
        if not isinstance(time_object, datetime):
            raise TypeError('should be a datetime object.')
        return time_object
