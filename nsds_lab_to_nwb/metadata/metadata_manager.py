import os
import io
import yaml

class MetadataManager:
    '''Manages metadata for NWB file builder
    '''

    def __init__(self, metadata_path: str):
        self.__validate(metadata_path)
        self.metadata_path = metadata_path
        self.metadata = self.__get_metadata(metadata_path)

    def __validate():
        # check if the files exist
        pass

    def __get_metadata():
        # extract metadata from file
        pass
