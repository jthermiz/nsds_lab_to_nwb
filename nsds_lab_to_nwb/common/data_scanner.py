import os

from nsds_lab_to_nwb.common.dataset import Dataset


class DataScanner():
    '''
    Defines input path structure and stores relevant paths in a Dataset object.
    This is a base class for AuditoryDataScanner and BehaviorDataScanner classes.
    '''
    def __init__(self, animal_name, block,
                 data_path: str = '',
                 ):
        self.data_path = data_path
        self.animal_name = animal_name
        self.block = block

    def extract_dataset(self):
        # should be implemented for the specific experiment type
        raise NotImplementedError
