import re
import os
import numpy as np
import csv
import h5py
import scipy.io

from nsds_lab_to_nwb.metadata.stim_name_helper import check_stimulus_name


class StimValueExtractor():
    def __init__(self, stim_configs, stim_lib_path):
        self.stim_name = stim_configs['name']
        self.stim_values_command = stim_configs.get('stim_values', None)
        self.stim_lib_path = stim_lib_path

    def extract(self):
        if self.stim_values_command is None:
            return None

        stim_values_command = self.stim_values_command
        if 'tone_stimulus_values' in stim_values_command:
            extractor, filename = self.__parse_command(stim_values_command)
            if extractor != 'tone_stimulus_values':
                raise ValueError('parsing error')
            stim_values_path = self._get_stim_values_path(filename)
            stim_values = tone_stimulus_values(stim_values_path)
        if 'timit_stimulus_values' in stim_values_command:
            extractor, filename = self.__parse_command(stim_values_command)
            if extractor != 'timit_stimulus_values':
                raise ValueError('parsing error')
            stim_values_path = self._get_stim_values_path(filename)
            stim_values = timit_stimulus_values(stim_values_path)
        if 'gen_tone_stim_vals' in stim_values_command:
            extractor, _ = self.__parse_command(stim_values_command)
            if extractor != 'gen_tone_stim_vals':
                raise ValueError('parsing error')
            stim_values = gen_tone_stim_vals()
        if 'np.ones' in stim_values_command:
            stim_values = eval(stim_values_command)

        return stim_values

    def _get_stim_values_path(self, path_from_metadata):
        # prioritize path from list_of_stimuli.yaml in this package
        _, stim_info = check_stimulus_name(self.stim_name)
        path_from_los = stim_info['stim_values_path']
        if len(path_from_los) > 0:
            return os.path.join(self.stim_lib_path, path_from_los)

        # if empty path in list_of_stimuli.yaml, use metadata input
        return os.path.join(self.stim_lib_path, path_from_metadata)

    def __parse_command(self, command):
        ''' return (a_a_a, b.b.b) by parsing string 'a_a_a(b.b.b)' '''
        res = re.match('(\S+)\((\S+)\)', command)
        return (res.group(1), res.group(2))


def tone_stimulus_values(mat_file_path):
    ''' adapted from mars.configs.block_directory '''
    try:
        with h5py.File(mat_file_path, 'r') as sio:
            stim_vals = sio['stimVls'][:].astype(int)
    except OSError:
        # if we get 'OSError: Unable to open file (File signature not found)'
        # this mat file may be from an earlier MATLAB version
        # and is not in HDF5 format.
        sio = scipy.io.loadmat(mat_file_path)
        stim_vals = sio['stimVls'][:].astype(int)
    stim_vals[0,:] = stim_vals[0,:] + 8
    return stim_vals


def timit_stimulus_values(csv_file_path):
    ''' adapted from mars.configs.block_directory '''
    # NOTE: this file timit998.txt is just a list of wav files.
    # TODO: also load from these wav files.
    stim_vals = []
    with open(csv_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stim_vals.append(row['sample_id'])
    return stim_vals


def gen_tone_stim_vals():
    ''' exact copy from mars.configs.block_directory '''
    frqs = np.array([500, 577, 666, 769, 887, 1024, 1182,
        1364, 1575, 1818, 2098, 2421, 2795, 3226, 3723,
        4297, 4960, 5725, 6608, 7627, 8803, 10160, 11727,
        13535, 15622, 18031, 20812, 24021, 27725, 32000])
    amps = np.arange(1,9)
    frqset, ampset = np.meshgrid(frqs,amps)
    frq_amp_pairs = np.array([ampset.flatten(), frqset.flatten()]).T
    np.random.seed(seed=1234) #Insure that the same order is produced with each call.
    shuffle_inds1 = np.random.permutation(np.arange(frq_amp_pairs.shape[0]))
    shuffle_inds2 = np.random.permutation(np.arange(frq_amp_pairs.shape[0]))
    stim_vals = np.concatenate((frq_amp_pairs[shuffle_inds1,:],frq_amp_pairs[shuffle_inds2,:]),axis=0)
    return stim_vals.T
