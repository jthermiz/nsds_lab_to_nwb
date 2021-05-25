import tdt

class TDTReader():
    """TDT interface
    """
    def __init__(self, path, verbose=False, channels=None):
        """

        Args:
            path (str): path to tdt folder
            verbose (bool, optional): whether to print debugging statements. Defaults to False.
            channels (list, optional): list of channel ids to import. Defaults to None.
        """
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
        x = list(self.tdt_obj['streams'].__dict__.items())
        streams = [e[0] for e in x]
        return streams
    
    def get_metadata(self, stream):
        """Get specified stream metadata

        Args:
            stream (string): stream name

        Returns:
            meta (dict): dictionary containing stream recording parameters
        """
        meta = {}
        meta['sample_rate'] = self.tdt_obj['streams'][stream]['fs']
        meta['channel_ids'] = self.tdt_obj['streams'][stream]['channel']
        meta['num_channels'], meta['num_samples'] = self.tdt_obj['streams'][stream]['data'].shape
        return meta        
    
    def get_data(self, stream):
        """Get specified stream data

        Args:
            stream (string): stream name

        Returns:
            mat, meta (np-array, dict): Returns tuple of data matrix (wide form) 
                                        and metadata dictionary
        """
        mat = self.tdt_obj['streams'][stream]['data']
        meta = self.get_metadata(stream)
        return mat, meta

    def get_events(self):
        """Get event onset markers

        Returns:
            events (list): list of samples where an event occured
        """
        events = self.tdt_obj['epocs']['mark']['onset']
        return events
    
