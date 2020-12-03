from nsds_lab_to_nwb.components.htk.htk_manager import HtkManager

class HtkOriginator():
    def __init__(self, dataset, metadata):
        self.dataset = dataset
        self.metadata = metadata

        self.htk_manager = HtkManager(self.dataset.raw_htk_path)

    def make(self, nwb_content, electrode_table_regions):
        for device_name, dev_conf in self.metadata['device'].items():
            if isinstance(dev_conf, str): # skip other annotations
                continue
            e_series = self.htk_manager.extract_raw_htk(device_name, dev_conf,
                                                        electrode_table_regions[device_name])
            nwb_content.add_acquisition(e_series)
