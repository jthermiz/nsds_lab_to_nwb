import tdt
import warnings


class TDTReader:
    """TDT interface

    Parameters
    ----------
    path: str
        Path to tdt folder
    verbose: bool, optional
        Whether to print debugging statements. Defaults to False.
    channels: list, optional
        List of channel ids to import. Defaults to None.
    """
    def __init__(self, path, verbose=False, channels=None):
        self.path = path
        self.channels = channels
        self.verbose = verbose

        if channels is None:
            self.tdt_obj = tdt.read_block(path)
        else:
            self.tdt_obj = tdt.read_block(path, channel=channels)

        self.streams = self.get_streams()
        self.block_name = self.tdt_obj['info']['blockname']
        self.start_time = self.tdt_obj['info']['utc_start_time']

        if verbose:
            print('Stream list:')
            print(self.streams)

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
        stream_exist = self.check_stream(stream)
        if stream_exist:
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
        else:
            return None

    def check_stream(self, stream):
        """Checks to see if user specified stream exists in data

        Args:
            stream (string): stream name

        Returns:
            stream_available (bool): whether stream exisits
        """
        stream_available = True
        if stream not in self.streams:
            error_message = 'Device or stream not found. Available streams: '
            stream_available = False
            for stream in self.streams:
                error_message += stream + ', '
            warnings.warn(error_message)
        return stream_available

    def get_data(self, stream):
        """Get specified stream data

        Args:
            stream (string): stream name

        Returns:
            mat, meta (np-array, dict): Returns tuple of data matrix (wide form)
                                        and metadata dictionary (if no stream returns None)
        """
        stream_exisit = self.check_stream(stream)
        if stream_exisit:
            mat = self.tdt_obj['streams'][stream]['data']
            meta = self.get_metadata(stream)
            return mat, meta
        else:
            return None

    def get_events(self):
        """Get event onset markers

        Returns:
            events (list): list of samples where an event occured
        """
        events = self.tdt_obj['epocs']['mark']['onset']
        return events
