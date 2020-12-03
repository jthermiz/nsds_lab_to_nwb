import os
from scipy.io import wavfile

from pynwb import TimeSeries


class WavManager():
    def __init__(self, stim_path, stim_configs):
        self.stim_path = stim_path
        self.stim_configs = stim_configs

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
        if stim_name == 'tone150':
            return os.path.join(stim_path,
                'Tone150/freq_resp_area_stimulus_signal_flo500Hz_fhi32000Hz_nfreq30_natten1_nreps150_fs96000.wav')
        if stim_name == 'timit':
            return os.path.join(stim_path,
                'TIMIT/timit998s.wav')
        if stim_name == 'tone':
            return os.path.join(stim_path,
                'Tone/stimulus_signal_03202013.wav')
        if stim_name == 'wn2':
            return os.path.join(stim_path,
                'WN/tb_noise_burst_stim_fs96kHz_signal.wav')
        if stim_name == 'dmr':
            return os.path.join(stim_path,
                'DMR/dmr-500flo-40000fhi-4SM-40TM-40db-96khz-48DF-15min.wav')
        raise ValueError('unknown stimulus')
