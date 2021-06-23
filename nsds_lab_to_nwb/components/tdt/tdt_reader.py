import logging.config
import tdt

logger = logging.getLogger(__name__)


class TDTReader:
    """TDT interface

    Parameters
    ----------
    path: str
        Path to TDT folder
    dev_conf: (dict) metadata for the device.
        nwb_builder.metadata['device'][device_name]. Not used for TDT.
    channels: list, optional
        List of channel ids to import. Defaults to None.
    """
    def __init__(self, path, dev_conf, channels=None):
        self.path = path
        self.channels = channels

        if channels is None:
            self.tdt_obj = tdt.read_block(path)
        else:
            self.tdt_obj = tdt.read_block(path, channel=channels)

        self.streams = self.get_streams()
        self.block_name = self.tdt_obj['info']['blockname']
        self.start_time = self.tdt_obj['info']['utc_start_time']

        logger.info('Streams: ' + ', '.join(self.streams))

    def get_streams(self):
        """Get TDT all stream names

        Returns:
            streams (list): stream names
        """
        streams = list(self.tdt_obj['streams'].keys())
        return streams

    def get_metadata(self, stream):
        """Get specified stream metadata

        Args:
            stream (string): stream name

        Returns:
            meta (dict): dictionary containing stream recording parameters (if no stream returns None)
        """
        self.check_stream(stream)
        meta = {}
        meta['sample_rate'] = self.tdt_obj['streams'][stream]['fs']
        meta['channel_ids'] = self.tdt_obj['streams'][stream]['channel']
        meta['start_time'] = self.tdt_obj['info']['utc_start_time']
        data_shape = self.tdt_obj['streams'][stream]['data'].shape
        if len(data_shape) == 1:
            meta['num_samples'] = data_shape[0]
            meta['num_channels'] = 1
        else:
            meta['num_channels'], meta['num_samples'] = data_shape
        return meta

    def check_stream(self, stream):
        """Checks to see if user specified stream exists in data

        Args:
            stream (string): stream name

        Returns:
            stream_available (bool): whether stream exisits
        """
        if stream not in self.streams:
            error_message = 'Device or stream not found. Available streams: ['
            error_message += ', '.join(self.streams)
            error_message += ']'
            raise ValueError(error_message)

    def get_data(self, stream):
        """Get specified data

        Parameters
        ----------
        stream: str
            Stream name

        Returns
        -------
        data: ndarray
            Data array
        meta: dict
            Meta data for the data array.
        """
        self.check_stream(stream)
        data = self.tdt_obj['streams'][stream]['data'].T
        meta = self.get_metadata(stream)
        return data, meta

    def get_events(self):
        """Get event onset markers

        Returns:
            events (list): list of samples where an event occured
        """
        events = self.tdt_obj['epocs']['mark']['onset']
        return events
