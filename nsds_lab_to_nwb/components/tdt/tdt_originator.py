from nsds_lab_to_nwb.components.tdt.tdt_manager import TdtManager

class TdtOriginator():
    def __init__(self, dataset, metadata):
        self.dataset = dataset      # this should have all relavant paths
        self.metadata = metadata    # this should have all relevant metadata

        self.tdt_manager = TdtManager(self.dataset.raw_tdt_path)

    def make(self, nwb_content, electrode_table_regions):
        for device_name, dev_conf in self.metadata['device'].items():
            if isinstance(dev_conf, str): # skip other annotations
                continue
            e_series = self.tdt_manager.extract_tdt(device_name,
                                                    dev_conf,
                                                    electrode_table_regions[device_name])
            if e_series is not None:
                nwb_content.add_acquisition(e_series)
