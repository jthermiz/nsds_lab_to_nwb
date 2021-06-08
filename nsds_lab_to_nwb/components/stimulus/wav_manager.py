import os
from scipy.io import wavfile
from importlib_resources import files

from pynwb import TimeSeries

from nsds_lab_to_nwb.components.stimulus.stim_value_extractor import StimValueExtractor
from nsds_lab_to_nwb.metadata.stim_name_helper import check_stimulus_name
from nsds_lab_to_nwb.utils import get_stim_lib_path
from nsds_lab_to_nwb import _data


class WavManager():
    def __init__(self, stim_lib_path, stim_configs):
        self.stim_name = stim_configs['name']
        self.stim_lib_path = get_stim_lib_path(stim_lib_path)
        self.stim_configs = stim_configs
        self.__load_stim_values()

    def get_stim_wav(self, first_mark, name='recorded_mark'):
        if self.stim_name == 'wn1':
            return None
        return self._get_stim_wav(self.get_stim_file(self.stim_name, self.stim_lib_path),
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
                            starting_time=starting_time,
                            unit='Volt',
                            rate=rate,
                            description='The neural recording aligned stimulus track.')
        return stim_time_series

    @staticmethod
    def get_stim_file(stim_name, stim_path):
        _, stim_info = check_stimulus_name(stim_name)
        return os.path.join(stim_path, stim_info['audio_path'])

    @staticmethod
    def append_stim_folder(stim_name, path):
        if stim_name == 'tone150':
            return os.path.join(path, 'Tone150')
        elif stim_name == 'timit':
            return os.path.join(path, 'TIMIT')
        elif stim_name == 'tone':
            return os.path.join(path, 'Tone')
        elif stim_name == 'wn2':
            return os.path.join(path, 'WN')
        elif stim_name == 'dmr':
            return os.path.join(path, 'DMR')
        else:
            raise ValueError('unknown stimulus')

    def __load_stim_values(self):
        '''load stim_values from .mat or .csv files,
        or generate using original script (mars/configs/block_directory.py)
        '''
        if not ('stim_values' in self.stim_configs):
            self.stim_configs['stim_values'] = None
        else:
            sve = StimValueExtractor(self.stim_configs['stim_values'],
                                     self.append_stim_folder(self.stim_name,
                                                             self.stim_lib_path))
            self.stim_configs['stim_values'] = sve.extract()
