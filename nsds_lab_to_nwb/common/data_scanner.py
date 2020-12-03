import os
from nsds_lab_to_nwb.common.dataset import Dataset

class DataScanner():
    def __init__(self, animal_name, block,
                 data_path: str = '',
                 stim_path: str = '',
                 htk_path: str = '',
                 ):
        self.data_path = data_path
        self.animal_name = animal_name
        self.block = block
        self.stim_path = stim_path
        self.htk_path = htk_path

        self.block_dir = os.path.join(self.htk_path,
                                    self.animal_name, 
                                    self.animal_name + '_' + self.block + '/')

    def extract_dataset(self):
        raw_htk_path = self.__get_raw_htk_path()
        mark_path = self.__find_mark_track()
        return Dataset(data_path=self.data_path, 
                       animal_name=self.animal_name,
                       block=self.block,
                       block_dir=self.block_dir,
                       raw_htk_path=raw_htk_path,
                       mark_path=mark_path,
                       stim_path=self.stim_path,
                       )

    def __find_mark_track(self, mark='mrk11.htk'):
        return os.path.join(self.block_dir, mark)

    def __get_raw_htk_path(self, raw='RawHTK/'):
        return os.path.join(self.block_dir, raw)
