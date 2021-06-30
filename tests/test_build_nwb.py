import os
import unittest

from nsds_lab_to_nwb.nwb_builder import NWBBuilder
from nsds_lab_to_nwb.metadata.metadata_manager import MetadataManager
from nsds_lab_to_nwb.utils import (split_block_folder, get_data_path,
                                   get_metadata_lib_path, get_stim_lib_path)


class TestCase_Build_NWB(unittest.TestCase):

    data_path = get_data_path()
    metadata_save_path = '_test/'
    out_path = '_test/'

    def test_build_nwb_single_block(self):
        ''' build NWB but do not write file to disk '''
        # --------------------------------------------------------------
        # currently failing blocks:
        # new test blocks: RVG16_{B02, B04, B05, B06, B07, B08, B09, B10}
        #                       B02, B04, B05: tone diagnostic (no metadata yaml)
        #                       B06: unable to open file Tone/Tone.stimVls.mat
        #                       B07: unable to open file Tone150/Tone150.stimVls.mat
        #                       B08: FileNotFoundError TIMIT/timit998.txt
        #                       B09: stimulus type 'nan' not found
        #                       B10: ValueError: Unknown stimulus type '{stim_name}' for mark tokenizer
        # legacy test block: R56_B10: metadata yaml not found in data_path
        block_folder = 'R56_B10'
        use_htk = False
        # --------------------------------------------------------------
        self.__build_nwb_content(block_folder, use_htk)

    def __build_nwb_content(self, block_folder, use_htk):
        ''' build NWB but do not write file to disk '''
        _, animal_name, _ = split_block_folder(block_folder)
        block_metadata_path = os.path.join(self.data_path, animal_name, block_folder,
                                           f"{block_folder}.yaml")
        nwb_builder = NWBBuilder(data_path=self.data_path,
                                 block_folder=block_folder,
                                 save_path=self.out_path,
                                 block_metadata_path=block_metadata_path,
                                 metadata_save_path=self.metadata_save_path,
                                 use_htk=use_htk)
        nwb_content = nwb_builder.build()


if __name__ == '__main__':
    unittest.main()
