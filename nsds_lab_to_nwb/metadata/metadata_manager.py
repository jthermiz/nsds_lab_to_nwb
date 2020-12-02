import os
import io
import json
import yaml

class MetadataManager:
    '''Manages metadata for NWB file builder
    '''

    def __init__(self, metadata_path: str):
        self.metadata_path = metadata_path
        self.metadata = self.extract_metadata(metadata_path)

    @staticmethod
    def extract_metadata(metadata_path):
        with open(metadata_path, 'r') as stream:
            metadata_dict = yaml.safe_load(stream)
            metadata = json.loads(json.dumps(metadata_dict), parse_int=str, parse_float=str)
            return metadata
