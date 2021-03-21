import os

from nsds_lab_to_nwb.common.dataset import Dataset
from nsds_lab_to_nwb.common.data_scanner import DataScanner


class BehaviorDataScanner(DataScanner):
    def __init__(self, animal_name, block,
                 data_path: str = '',
                 video_path=None,
                 ):
        DataScanner.__init__(self, animal_name, block, data_path=data_path)
        # this sets self.animal_name, self.block, and self.data_path

        # TODO: collect and pass relevant subdirectories. maybe video_path?
        self.video_path = video_path or os.path.join(self.data_path, 'Video/') # <<<< replace accordingly

    def extract_dataset(self):
        # TODO for behavior (reaching) data
        raise NotImplementedError
