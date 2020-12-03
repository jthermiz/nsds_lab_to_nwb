import os
import io
import json
import yaml

from nsds_lab_to_nwb.metadata.stim_value_extractor import StimValueExtractor


class MetadataManager:
    '''Manages metadata for NWB file builder
    '''

    def __init__(self,
                 metadata_path: str,
                 library_path: str,
                 animal_name = None
                 ):
        self.metadata_path = metadata_path
        self.library_path = library_path
        self.animal_name = animal_name

        self.yaml_lib_path = os.path.join(self.library_path, 'yaml/')
        self.stim_lib_path = os.path.join(self.library_path,
                                'configs_legacy/mars_configs/') # <<<< should move to a better subfolder
        self.metadata = self.extract_metadata()

    def extract_metadata(self):
        block_metadata = self.read_yaml(self.metadata_path)
        block_name = block_metadata.pop('name')
        if self.animal_name is None:
            self.animal_name = block_name.split('_')[0]

        metadata = {}
        metadata['block_name'] = block_name
        for key, value in block_metadata.items():
            if key == 'experiment':
                self.expand_experiment(metadata, value)
                continue
            if key == 'device':
                self.expand_device(metadata, value)
                continue
            if key == 'stimulus':
                self.expand_stimulus(metadata, value)
                continue
            # else:
            metadata[key] = value

        metadata['experiment_description'] = metadata['stimulus']['name'] + ' Stimulus Experiment'
        if not metadata['session_description']:
            metadata['session_description'] = metadata['experiment_description']
        return metadata

    def expand_experiment(self, metadata, filename, key='experiment'):
        ref_data = self.read_yaml(os.path.join(
                        self.yaml_lib_path, key, filename + '.yaml'))
        ref_data.pop('name')
        self.__check_subject(metadata)
        # add to top level
        metadata.update(ref_data)

    def expand_device(self, metadata, filename, key='device'):
        ref_data = self.read_yaml(os.path.join(
                        self.yaml_lib_path, key, filename + '.yaml'))
        self.__load_probes(ref_data)
        metadata[key] = ref_data

    def expand_stimulus(self, metadata, filename, key='stimulus'):
        ref_data = self.read_yaml(os.path.join(
                        self.yaml_lib_path, key, filename + '.yaml'))
        self.__load_stim_values(ref_data)
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
                device_metadata[key] = self.read_yaml(probe_path)

    def __load_stim_values(self, stimulus_metadata):
        '''load stim_values from .mat or .csv files,
        or generate using original script (mars/configs/block_directory.py)
        '''
        stimulus_metadata['stim_values'] = StimValueExtractor(
            stimulus_metadata['stim_values'], self.stim_lib_path
            ).extract()


    @staticmethod
    def read_yaml(file_path):
        with open(file_path, 'r') as stream:
            metadata_dict = yaml.safe_load(stream)
            metadata = json.loads(json.dumps(metadata_dict)) #, parse_int=str, parse_float=str)
            return metadata
