class StimulusTokenizer():
    """ Base Tokenizer class for auditory stimulus data
    """
    def __init__(self, block_name, stim_configs):
        self.block_name = block_name
        self.stim_configs = stim_configs

    def tokenize(self, nwb_content, mark_name='recorded_mark'):
        raise NotImplementedError('should be implemeted in inherited class')

    def __already_tokenized(self, nwb_content):
        raise NotImplementedError('should be implemeted in inherited class')

    def __get_stim_onsets(self, nwb_content, mark_name):
        raise NotImplementedError('should be implemeted in inherited class')

    def _get_end_time(self, nwb_content, mark_name):
        mark_dset = self.read_mark(nwb_content, mark_name=mark_name)
        end_time = mark_dset.num_samples/mark_dset.rate
        return end_time

    def read_mark(self, nwb_content, mark_name='recorded_mark'):
        return nwb_content.stimulus[mark_name]
        
    def read_raw(self, nwb_content, device_name):
        """
        Read a raw dataset from the currently open nwb file
        """
        return nwb_content.acquisition[device_name]
