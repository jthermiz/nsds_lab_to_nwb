import os
import csv
import pandas as pd
from ..utils import (get_metadata_lib_path, get_stim_lib_path,
                     split_block_folder)

from nsds_lab_to_nwb.common.io import read_yaml, write_yaml, csv_to_dict


_DEFAULT_EXPERIMENT_TYPE = 'auditory'  # for legacy sessions

class LegacyMetadataReader:
    ''' Reads metadata input for old experiments.
    '''
    def __init__(self,
                block_metadata_path: str,
                library_path: str,
                block_folder: str,
                ):
        self.block_metadata_path = block_metadata_path
        self.library_path = library_path
        self.block_folder = block_folder

    def read_block_metadata(self):
        # direct input from the block yaml file (not yet expanded)
        self.block_metadata_input = read_yaml(self.block_metadata_path)
        return self.block_metadata_input


class MetadataReader:
    ''' Reads metadata input for new experiments.
    '''
    def __init__(self,
                block_metadata_path: str,
                library_path: str,
                block_folder: str,
                ):
        self.block_metadata_path = block_metadata_path
        self.library_path = library_path
        self.block_folder = block_folder

    def read_block_metadata(self):
        # direct input from the block yaml file (not yet expanded)
        _, _, block_tag = split_block_folder(self.block_folder)
        block_id = int(block_tag[1:])   # the integer after the 'B'
        self.block_metadata_input = self.read_csv_row(self.block_metadata_path, block_id)

        # CAVEAT: keys 'name' and 'experiment_type' should not be expanded
        self.__extend_experiment_and_device_metadata_new_pipeline()
        return self.block_metadata_input

    @staticmethod
    def read_csv_row(file_path, block_id):
        all_blocks = pd.read_csv(file_path)
        blk_row = all_blocks.loc[all_blocks['block_id'] == block_id] # single row of DataFrame
        blk_dict = blk_row.to_dict(orient='records')[0] # a dict
        return blk_dict

    def __extend_experiment_and_device_metadata_new_pipeline(self):
        # this is somewhat ad hoc.
        # new metadata pipeline will be updated in the near future

        # unpack experiment
        experiment_metadata_path = os.path.join(
            os.path.dirname(self.block_metadata_path), 'meta_data.csv')
        experiment_metadata_input = csv_to_dict(experiment_metadata_path)

        device_metadata_input = self.__separate_device_metadata(experiment_metadata_input)
        self.block_metadata_input['experiment'] = experiment_metadata_input
        self.block_metadata_input['device'] = device_metadata_input

        # separate stimulus metadata
        if 'stim' in self.block_metadata_input:
            self.block_metadata_input['stimulus'] = {'name': self.block_metadata_input.pop('stim')}

    def __separate_device_metadata(self, metadata_input):
        device_metadata = {}
        for key in metadata_input.copy():
            if ('ecog_' in key) or ('poly_' in key):
                value = metadata_input.pop(key)
                if key == 'ecog_type':
                    device_metadata['ECoG'] = value
                if key == 'poly_type':
                    device_metadata['Poly'] = value
                device_metadata[key] = value
        return device_metadata


class MetadataManager:
    """Manages metadata for NWB file builder

    Parameters
    ----------
    block_metadata_path : str
        Path to block metadata file.
    metadata_lib_path : str
        Path to metadata library repo.
    stim_lib_path : str
        Path to stimulus library.
    block_folder : str
        Block specification.
    """
    def __init__(self,
                 block_metadata_path: str,
                 metadata_lib_path=None,
                 stim_lib_path=None,
                 block_folder=None,
                 ):
        self.block_metadata_path = block_metadata_path
        self.metadata_lib_path = get_metadata_lib_path(metadata_lib_path)
        self.stim_lib_path = get_stim_lib_path(stim_lib_path)
        self.block_folder = block_folder
        self.surgeon_initials, self.animal_name, self.block_tag = split_block_folder(block_folder)
        self.__detect_legacy_block()

        if self.legacy_block:
            self.reader = LegacyMetadataReader(
                            block_metadata_path=self.block_metadata_path,
                            library_path=self.metadata_lib_path,
                            block_folder=block_folder)
        else:
            self.reader = MetadataReader(
                            block_metadata_path=self.block_metadata_path,
                            library_path=self.metadata_lib_path,
                            block_folder=block_folder)

        self.read_block_metadata()

        # new requirement for nsdslab data: experiment_type
        self.experiment_type = self.block_metadata_input.pop('experiment_type', _DEFAULT_EXPERIMENT_TYPE)

        # paths to metadata/stimulus library
        self.yaml_lib_path = os.path.join(self.metadata_lib_path, self.experiment_type, 'yaml/')

    def __detect_legacy_block(self):
        # detect which pipeline is used, based on metadata format
        _, ext = os.path.splitext(self.block_metadata_path)
        if ext in ('.yaml', '.yml'):
            self.legacy_block = True
        elif ext == '.csv':
            self.legacy_block = False
        else:
            raise ValueError('unknown block metadata format')

    def read_block_metadata(self, write_yaml_file=True):
        self.block_metadata_input = self.reader.read_block_metadata()

        if write_yaml_file:
            # export block_metadata_input for inspection
            # can set write_yaml_file to False once metadata pipeline is stable
            write_yaml(f'_test/{self.block_folder}_block_metadata_input.yaml', self.block_metadata_input)

    def extract_metadata(self):
        metadata = {}
        metadata['block_name'] = self.block_folder
        metadata['experiment_type'] = self.experiment_type

        # # expand metadata parts by extracting from library
        for key, value in self.block_metadata_input.items():
            if key == 'experiment':
                self.expand_experiment(metadata, value)
                continue
            if key == 'device':
                self.expand_device(metadata, value)
                continue
            if key == 'stimulus':
                if self.experiment_type != 'auditory':
                    raise ValueError('experiment type mismatch')
                self.expand_stimulus(metadata, value)
                continue
            metadata[key] = value

        # set experiment description
        if self.experiment_type == 'auditory':
            metadata['experiment_description'] = metadata['stimulus']['name'] + ' Stimulus Experiment'
        elif self.experiment_type == 'behavior':
            metadata['experiment_description'] = 'Reaching Experiment' # <<<< any additional specification?
        else:
            metadata['experiment_description'] = 'Unknown'

        # set session description, if not already existing
        if not metadata.get('session_description', None):
            metadata['session_description'] = metadata['experiment_description']
        return metadata

    def extract_metadata_old(self):
        metadata = {}
        metadata['block_name'] = self.block_folder
        metadata['experiment_type'] = self.experiment_type

        # expand metadata parts by extracting from library
        for key, value in self.block_metadata_input.items():
            if key == 'experiment':
                self.expand_experiment(metadata, value)
                continue
            if key == 'device':
                self.expand_device(metadata, value)
                continue
            if key == 'stimulus':
                if self.experiment_type != 'auditory':
                    raise ValueError('experiment type mismatch')
                self.expand_stimulus(metadata, value)
                continue
            # else:
            metadata[key] = value

        # set experiment description
        if self.experiment_type == 'auditory':
            metadata['experiment_description'] = metadata['stimulus']['name'] + ' Stimulus Experiment'
        elif self.experiment_type == 'behavior':
            metadata['experiment_description'] = 'Reaching Experiment' # <<<< any additional specification?
        else:
            metadata['experiment_description'] = 'Unknown'

        # set session description, if not already existing
        if not metadata['session_description']:
            metadata['session_description'] = metadata['experiment_description']
        return metadata

    def expand_experiment(self, metadata, filename, key='experiment'):
        if isinstance(filename, str):
            ref_data = read_yaml(os.path.join(
                            self.yaml_lib_path, key, filename + '.yaml'))
        elif isinstance(filename, dict):
            ref_data = filename
        ref_data.pop('name', None)
        metadata.update(ref_data)  # add to top level
        self.__check_subject(metadata)

    def expand_device(self, metadata, filename, key='device'):
        if isinstance(filename, str):
            ref_data = read_yaml(os.path.join(
                            self.yaml_lib_path, key, filename + '.yaml'))
        elif isinstance(filename, dict):
            ref_data = filename
        self.__load_probes(ref_data)
        metadata[key] = ref_data

    def expand_stimulus(self, metadata, filename, key='stimulus'):
        if isinstance(filename, str):
            ref_data = read_yaml(os.path.join(
                            self.yaml_lib_path, key, filename + '.yaml'))
        elif isinstance(filename, dict):
            ref_data = filename

        ref_data['stim_lib_path'] = self.stim_lib_path # pass stim library path (ad hoc)
        metadata[key] = ref_data

    def __check_subject(self, metadata):
        if 'subject' not in metadata:
            metadata['subject'] = {}
        if 'subject id' not in metadata['subject']:
            metadata['subject']['subject id'] = self.animal_name
        if 'species' not in metadata['subject']:
            if metadata['subject']['subject id'][0] == 'R':
                metadata['subject']['species'] = 'Rat'
        for key in ('description', 'genotype', 'sex'):
            if key not in metadata['subject']:
                metadata['subject'][key] = 'Unknown'

    def __load_probes(self, device_metadata):
        for key, value in device_metadata.items():
            if key in ('ECoG', 'Poly'):
                probe_path = os.path.join(self.yaml_lib_path, 'probe', value + '.yaml')
                device_metadata[key] = read_yaml(probe_path)
