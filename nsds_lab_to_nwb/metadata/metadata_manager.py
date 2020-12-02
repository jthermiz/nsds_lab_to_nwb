import os
import io
import json
import yaml

class MetadataManager:
    '''Manages metadata for NWB file builder
    '''

    def __init__(self, metadata_path: str, library_path: str):
        self.metadata_path = metadata_path
        self.library_path = library_path
        self.metadata = self.extract_metadata()

    def extract_metadata(self):
        block_metadata = self.read_yaml(self.metadata_path)

        metadata = {}
        for key, value in block_metadata.items():
            if key == 'name':
                metadata['session_id'] = value
            if key in ('experiment', 'device', 'stimulus'):
                ref_data = self.read_yaml(os.path.join(
                                self.library_path, key, value + '.yaml'))
                if key == 'experiment':
                    ref_data.pop('name')
                    metadata.update(ref_data) # add to top level
                    self.__check_subject(metadata)
                    continue
                if key == 'device':
                    self.__load_probes(ref_data)
                if key == 'stimulus':
                    self.__load_stim_values(ref_data)
                metadata[key] = ref_data
            else:
                metadata[key] = value
        return metadata

    def __check_subject(self, metadata):
        if 'subject' not in metadata:
            metadata['subject'] = {}
        if 'subject id' not in metadata['subject']:
            metadata['subject']['subject id'] = metadata['session_id'].split('_')[0]
        for key in ('description', 'genotype', 'sex', 'species'):
            if key not in metadata['subject']:
                metadata['subject'][key] = ''

    def __load_probes(self, device_metadata):
        for key, value in device_metadata.items():
            if key in ('ECoG', 'Poly'):
                probe_path = os.path.join(self.library_path, 'probe', value + '.yaml')
                # device_metadata[key] = str(probe_path) # just save the filename?
                device_metadata[key] = self.read_yaml(probe_path)

    def __load_stim_values(self, stimulus_metadata):
        # should load stim_values from .mat files
        # see: mars/configs/block_directory.py
        pass

    @staticmethod
    def read_yaml(file_path):
        with open(file_path, 'r') as stream:
            metadata_dict = yaml.safe_load(stream)
            metadata = json.loads(json.dumps(metadata_dict)) #, parse_int=str, parse_float=str)
            return metadata
