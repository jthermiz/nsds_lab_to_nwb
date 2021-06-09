import os
from scipy.io import wavfile

from pynwb import TimeSeries

from nsds_lab_to_nwb.common.io import read_yaml
from nsds_lab_to_nwb.components.stimulus.stim_value_extractor import StimValueExtractor


class WavManager():
    def __init__(self, stim_path, stim_configs):
        self.stim_path = stim_path
        self.stim_configs = stim_configs
        self.__load_stim_values(self.stim_configs)

    def get_stim_wav(self, first_mark, name='recorded_mark'):
        stim_name = self.stim_configs['name']
        if stim_name == 'wn1':
            return None
        return self._get_stim_wav(self.get_stim_file(stim_name, self.stim_path),
                                  first_mark)

    def _get_stim_wav(self, stim_file, first_recorded_mark, name='raw_stimulus'):
        ''' get the raw wav stimulus track '''
        # find starting time
        starting_time = (first_recorded_mark
                            - self.stim_configs['mark_offset']  # adjust for mark offset
                            - self.stim_configs['first_mark'])  # time between stimulus DVD start and the first mark

        # Read the stimulus wav file
        stim_wav_fs, stim_wav = wavfile.read(stim_file)

        # Create the stimulus timeseries
        rate = float(stim_wav_fs)
        stim_time_series = TimeSeries(name=name,
                            data=stim_wav,
                            unit='Volts',
                            starting_time=starting_time,
                            rate=rate,
                            description='The neural recording aligned stimulus track.')
        return stim_time_series

    @staticmethod
    def get_stim_file(stim_name, stim_path):
        stim_directory = read_yaml('../../_data/list_of_stimuli.yaml')

        if stim_name in stim_directory.keys():
            # if there is a matching key, just read the corresponding entry
            stim_info = stim_directory[stim_name]
            return os.path.join(stim_path, stim_info['audio_path'])

        # if stim_name does not match any key, try the alternative names
        for key, stim_info in stim_directory.items():
            for alt_name in stim_info['alt_names']:
                if stim_name == alt_name:
                    return os.path.join(stim_path, stim_info['audio_path'])

        raise ValueError('cannot find stimulus in list_of_stimuli.yaml')

    def __load_stim_values(self, stimulus_metadata):
        '''load stim_values from .mat or .csv files,
        or generate using original script (mars/configs/block_directory.py)
        '''
        if not ('stim_values' in stimulus_metadata):
            stimulus_metadata['stim_values'] = None
            return

        stimulus_metadata['stim_values'] = StimValueExtractor(
            stimulus_metadata['stim_values'], stimulus_metadata['stim_lib_path']
            ).extract()
