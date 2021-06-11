import importlib.resources
import os

from nsds_lab_to_nwb.common.io import read_yaml

def check_stimulus_name(stim_name_input):
    with importlib.resources.path('nsds_lab_to_nwb.metadata.resources', 'list_of_stimuli.yaml') as data_path:
        stim_directory = read_yaml(data_path)

    if stim_name_input in stim_directory.keys():
        # if there is a matching key, just read the corresponding entry
        return stim_name_input, stim_directory[stim_name_input]
    # if stim_name does not match any key, try the alternative names
    for key, stim_info in stim_directory.items():
        for alt_name in stim_info['alt_names']:
            if stim_name_input == alt_name:
                return key, stim_info
