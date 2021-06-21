import logging
import os
import csv
import numpy as np
import pandas as pd
from nsds_lab_to_nwb.utils import (get_metadata_lib_path, get_stim_lib_path,
                                   split_block_folder)

from nsds_lab_to_nwb.common.io import read_yaml, write_yaml, csv_to_dict
from nsds_lab_to_nwb.metadata.keymap_helper import apply_keymap
from nsds_lab_to_nwb.metadata.stim_name_helper import check_stimulus_name


_DEFAULT_EXPERIMENT_TYPE = 'auditory'

logger = logging.getLogger(__name__)


class MetadataReader:
    ''' Reads metadata input for new experiments.
    '''
    def __init__(self,
                block_metadata_path: str,
                library_path: str,
                block_folder: str,
                metadata_save_path=None,
                ):
        self.block_metadata_path = block_metadata_path
        self.library_path = library_path
        self.block_folder = block_folder
        self.metadata_save_path = metadata_save_path

    def read(self):
        self.metadata_input = self.load_metadata_source()
        if self.metadata_save_path is not None:
            write_yaml(f'{self.metadata_save_path}/{self.block_folder}_metadata_input.yaml',
                       self.metadata_input)

        self.parse()
        self.common_check()
        self.extra_cleanup()
        if self.metadata_save_path is not None:
            write_yaml(f'{self.metadata_save_path}/{self.block_folder}_metadata_input_clean.yaml',
                       self.metadata_input)

        return self.metadata_input

    def load_metadata_source(self):
        _, ext = os.path.splitext(self.block_metadata_path)
        if ext in ('.yaml', '.yml'):
            metadata_input = read_yaml(self.block_metadata_path)
        else:
            metadata_input = self._temporary_load_from_csv()
        return metadata_input

    def parse(self):
        self.metadata_input = apply_keymap(self.metadata_input.copy(),
                                           keymap_file='metadata_keymap')

    def common_check(self):
        ''' make sure that core fields exist before further expanding metadata components.
        common for both new and legacy pipelines.
        '''
        if 'subject' not in self.metadata_input:
            self.metadata_input['subject'] = {}

        device_metadata = self.metadata_input['device']
        for key in ('ECoG', 'Poly'):
            # required for ElectrodeGroup component
            if 'description' not in device_metadata[key]:
                device_metadata[key]['description'] = device_metadata[key]['name']
            if 'location' not in device_metadata[key]:
                # NEED: anatomical location in the brain, such as 'V1' or 'CA3'
                # perhaps something like 'AC' or 'A1' in our cases?
                device_metadata[key]['location'] = ''
            if 'location_details' not in device_metadata[key]:
                # more quantitative information
                device_metadata[key]['location_details'] = ''

            # required for Electrode component
            if 'imp' not in device_metadata[key]:
                # TODO: include impedance value
                device_metadata[key]['imp'] = np.nan
            if 'filtering' not in device_metadata[key]:
                device_metadata[key]['filtering'] = (
                    'Low-Pass Filtered to Nyquist frequency'    # confirm!
                    )

    def extra_cleanup(self):
        # device
        device_metadata = self.metadata_input['device']
        ecog_lat_loc = device_metadata['ECoG'].pop('ecog_lat_loc', None)
        ecog_post_loc = device_metadata['ECoG'].pop('ecog_post_loc', None)
        if (ecog_lat_loc is not None) and (ecog_post_loc is not None):
            device_metadata['ECoG']['location_details'] = (
                f'{ecog_lat_loc} mm from lateral ridge '
                f'and {ecog_post_loc} mm from posterior ridge.'
                )
        device_metadata['Poly']['location_details'] = 'Within the ECoG grid.'   # fixed

    def _temporary_load_from_csv(self):
        # direct input from the block yaml file (not yet expanded)
        _, _, block_tag = split_block_folder(self.block_folder)
        block_id = int(block_tag[1:])   # the integer after the 'B'
        block_metadata_input = self.read_csv_row(self.block_metadata_path, block_id)

        # also load experiment-level metadata
        experiment_metadata_path = os.path.join(
            os.path.dirname(self.block_metadata_path), 'meta_data.csv')
        experiment_metadata_input = csv_to_dict(experiment_metadata_path)

        metadata_input = {}
        metadata_input['block'] = block_metadata_input
        metadata_input['experiment'] = experiment_metadata_input
        return metadata_input

    @staticmethod
    def read_csv_row(file_path, block_id):
        all_blocks = pd.read_csv(file_path)
        blk_row = all_blocks.loc[all_blocks['block_id'] == block_id] # single row of DataFrame
        blk_dict = blk_row.to_dict(orient='records')[0] # a dict
        return blk_dict


class LegacyMetadataReader(MetadataReader):
    ''' Reads metadata input for old experiments.
    '''
    def __init__(self,
                block_metadata_path: str,
                library_path: str,
                block_folder: str,
                metadata_save_path=None,
                ):
        MetadataReader.__init__(self, block_metadata_path, library_path,
                                      block_folder, metadata_save_path)

        self.experiment_type = 'auditory'   # for legacy auditory datasets

        # TODO: separate (experiment, device) metadata library as legacy
        self.legacy_lib_path = os.path.join(self.library_path, self.experiment_type, 'yaml/')

    def load_metadata_source(self):
        # direct input from the block yaml file (not yet expanded)
        metadata_input = read_yaml(self.block_metadata_path)

        # load from metadata library (legacy structure)
        for key in ('experiment', 'device'):
            logger.info(f'expanding {key} from legacy metadata library...')
            filename = metadata_input.pop(key)
            ref_data = read_yaml(
                os.path.join(self.legacy_lib_path, key, filename + '.yaml'))
            ref_data.pop('name', None)
            metadata_input.update(ref_data)
        return metadata_input

    def parse(self):
        self.metadata_input = apply_keymap(self.metadata_input.copy(),
                                           keymap_file='metadata_keymap_legacy')

    def extra_cleanup(self):
        # put bad_chs to right places
        bad_chs_dict = self.metadata_input['device'].pop('bad_chs', None)
        if bad_chs_dict is not None:
            for dev_name, bad_chs in bad_chs_dict.items():
                self.metadata_input['device'][dev_name]['bad_chs'] = bad_chs

        # final touches...
        if self.experiment_type == 'auditory':
            self.metadata_input['experiment_description'] = 'Auditory experiment'
        if ('session_description' not in self.metadata_input
                    or len(self.metadata_input['session_description']) == 0):
            self.metadata_input['session_description'] = (
                'Auditory experiment with {} stimulus'.format(self.metadata_input['stimulus']['name']))


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
    metadata_save_path : str (optional)
        Path to a directory where parsed metadata file(s) will be saved.
        Files are saved only if metadata_save_path is provided.
    experiment_type : str (optional)
        Experiment type within the NSDS Lab: 'auditory' (default) or 'behavior'.
    legacy_block : bool (optional)
        Indicates whether this is a legacy block.
        If not provided, auto-detect by the metadata file extension (CAVEAT: no longer accurate)

    """
    def __init__(self,
                 block_metadata_path: str,
                 metadata_lib_path=None,
                 stim_lib_path=None,
                 block_folder=None,
                 metadata_save_path=None,
                 experiment_type=_DEFAULT_EXPERIMENT_TYPE,
                 legacy_block=None,
                 ):
        self.block_metadata_path = block_metadata_path
        self.metadata_lib_path = get_metadata_lib_path(metadata_lib_path)
        self.stim_lib_path = get_stim_lib_path(stim_lib_path)
        self.block_folder = block_folder
        self.surgeon_initials, self.animal_name, self.block_tag = split_block_folder(block_folder)
        self.metadata_save_path = metadata_save_path
        self.experiment_type = experiment_type
        self.yaml_lib_path = os.path.join(self.metadata_lib_path, self.experiment_type, 'yaml/')
        self.__detect_legacy_block(legacy_block)

        if self.metadata_save_path is not None:
            os.makedirs(self.metadata_save_path, exist_ok=True)

        if self.legacy_block:
            self.metadata_reader = LegacyMetadataReader(
                            block_metadata_path=self.block_metadata_path,
                            library_path=self.metadata_lib_path,
                            block_folder=self.block_folder,
                            metadata_save_path=self.metadata_save_path)
        else:
            self.metadata_reader = MetadataReader(
                            block_metadata_path=self.block_metadata_path,
                            library_path=self.metadata_lib_path,
                            block_folder=self.block_folder,
                            metadata_save_path=self.metadata_save_path)

    def __detect_legacy_block(self, legacy_block=None):
        if (legacy_block is not None):
            self.legacy_block = legacy_block
            return

        # detect which pipeline is used, based on animal naming scheme
        if self.surgeon_initials is not None:
            self.legacy_block = False
        else:
            self.legacy_block = True

    def extract_metadata(self):
        metadata_input = self.metadata_reader.read()

        metadata = self._extract(metadata_input)

        if self.metadata_save_path is not None:
            write_yaml(f'{self.metadata_save_path}/{self.block_folder}_metadata_full.yaml',
                       metadata)

        return metadata

    def _extract(self, metadata_input):
        metadata_input['experiment_type'] = self.experiment_type

        metadata = {}
        metadata['block_name'] = self.block_folder

        input_block_name = metadata_input.pop('name', None)
        if (input_block_name is not None) and input_block_name != metadata['block_name']:
            metadata['block_name_in_source'] = input_block_name

        # extract and add metadata fields in this order
        for key in ('experimenter', 'lab', 'institution',
                    'experiment_description', 'session_description',
                    'subject', 'surgery', 'pharmacology', 'notes',
                    'experiment_meta', 'experiment_type',
                    'stimulus', 'block_meta',
                    'device'
                    ):
            value = metadata_input.pop(key, None)
            if value is None:
                continue
            if key == 'stimulus':
                self.__load_stimulus_info(value)
            if key == 'device':
                self.__load_probes(value)
            metadata[key] = value

        # extract all remaining fields
        for key, value in metadata_input.items():
            logger.info(f'WARNING - unknown metadata field {key}')
            metadata[key] = value

        # final validation
        self.__check_subject(metadata)

        return metadata

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

    def __load_stimulus_info(self, stimulus_metadata):
        stim_name, _ = check_stimulus_name(stimulus_metadata['name'])
        if stim_name != stimulus_metadata['name']:
            stimulus_metadata['alt_name'] = stimulus_metadata['name']
        stim_yaml_path = os.path.join(self.yaml_lib_path, 'stimulus', stim_name + '.yaml')
        stimulus_metadata.update(read_yaml(stim_yaml_path))

    def __load_probes(self, device_metadata):
        for key, value in device_metadata.items():
            if key in ('ECoG', 'Poly'):
                if isinstance(value, str):
                    device_metadata[key] = {'name': value}
                probe_name = device_metadata[key]['name']
                probe_path = os.path.join(self.yaml_lib_path, 'probe', probe_name + '.yaml')
                device_metadata[key].update(read_yaml(probe_path))

                # TODO/CONSIDER: apply offset to all poly ch_pos systematically?
                # (using device_metadata['Poly']['poly_ap_loc']
                # and device_metadata['Poly']['poly_dev_loc'])

                # format device description
                nchannels, device_type, manufacturer = (
                    device_metadata[key]['nchannels'],
                    device_metadata[key]['device_type'],
                    device_metadata[key]['manufacturer'])
                device_metadata[key]['description'] = (
                    f'{nchannels}-ch {key} '
                    # f'({device_type}) '
                    f'from {manufacturer}')
