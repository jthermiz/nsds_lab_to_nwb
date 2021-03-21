import tdt


class TdtHelper():
    def __init__(self, tdt_path, verbose=True, channels=None):

        if channels is None:
            self.tdt_data = tdt.read_block(tdt_path)
        else:
            self.tdt_data = tdt.read_block(tdt_path, channel=channels)

        self.streams = self.get_stream_list()
        
        if verbose:
            print('Stream list:')
            print(self.streams)

    def get_stream_list(self):
        x = list(self.tdt_data['streams'].__dict__.items())
        streams = [e[0] for e in x]
        return streams

    def get_stream_data(self, stream):
        mat = self.tdt_data['streams'][stream]['data']
        meta = {}
        meta['sample_rate'] = self.tdt_data['streams'][stream]['fs']
        meta['channel_ids'] = self.tdt_data['streams'][stream]['channel']
        return mat, meta
