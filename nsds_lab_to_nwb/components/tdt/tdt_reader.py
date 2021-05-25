import tdt

class TDTReader():
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
        x = list(self.tdt_obj['streams'].__dict__.items())
        streams = [e[0] for e in x]
        return streams
    
    def get_metadata(self, stream):
        meta = {}
        meta['sample_rate'] = self.tdt_obj['streams'][stream]['fs']
        meta['channel_ids'] = self.tdt_obj['streams'][stream]['channel']
        meta['num_channels'], meta['num_samples'] = self.tdt_obj['streams'][stream]['data'].shape
        return meta        
    
    def get_data(self, stream):
        mat = self.tdt_obj['streams'][stream]['data']
        meta = self.get_metadata(stream)
        return mat, meta

    def get_events(self):
        events = self.tdt_obj['epocs']['mark']['onset']
        return events
    
'''
#%% Test cases

data_directory = '/home/jhermiz/data/aer/RVG06_B03'
tobj = TDTReader(data_directory)
print(tobj)
# %%

data, meta = tobj.get_data('Wave')
print(data.shape)

# %%
print(meta)
# %%
events = tobj.get_events()
len(events)
# %%
streams = tobj.get_streams()
print(streams)

'''
