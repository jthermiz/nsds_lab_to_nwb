import unittest
import os

from nsds_lab_to_nwb.common.data_scanners import Dataset
from nsds_lab_to_nwb.components.time.session_time_extractor import SessionTimeExtractor
from nsds_lab_to_nwb.utils import get_data_path


class TestCase_SessionTimeExtractor(unittest.TestCase):

    data_path = get_data_path()

    def test_session_time_extractor_case1_TDT(self):
        ''' extract session start time from TDT files. '''
        block_name = 'RVG16_B01'
        block_metadata_path = '_data/RVG16/RVG16_B01.yaml'
        tdt_path = os.path.join(self.data_path, 'RVG16/RVG16_B01/')
        dataset = Dataset(block_name, self.data_path, tdt_path=tdt_path)
        metadata = {}
        st_extractor = SessionTimeExtractor(dataset, metadata)
        session_start_time = st_extractor.get_session_start_time()
        print(f'{block_name} (TDT): {session_start_time}')

    def test_session_time_extractor_case2_legacy_TDT(self):
        ''' extract session start time from TDT files. '''
        block_name = 'R56_B13'
        block_metadata_path = '_data/R56/R56_B13.yaml'
        tdt_path = os.path.join(self.data_path, 'R56/R56_B13/')
        dataset = Dataset(block_name, self.data_path, tdt_path=tdt_path)
        metadata = {}
        st_extractor = SessionTimeExtractor(dataset, metadata)
        session_start_time = st_extractor.get_session_start_time()
        print(f'{block_name} (TDT): {session_start_time}')

    def test_session_time_extractor_case3_legacy_HTK(self):
        ''' for the legacy HTK pipeline, just use a dummy start time. '''
        block_name = 'R56_B13'
        block_metadata_path = '_data/R56/R56_B13.yaml'
        dataset = Dataset(block_name, self.data_path, htk_path=None,
                                                      htk_mark_path=None)
        metadata = {}
        st_extractor = SessionTimeExtractor(dataset, metadata)
        session_start_time = st_extractor.get_session_start_time()
        print(f'{block_name} (HTK): {session_start_time}')


if __name__ == '__main__':
    unittest.main()
