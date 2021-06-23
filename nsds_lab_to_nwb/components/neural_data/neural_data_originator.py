import logging.config
from pynwb.ecephys import ElectricalSeries

from nsds_lab_to_nwb.components.htk.htk_reader import HTKReader
from nsds_lab_to_nwb.components.tdt.tdt_reader import TDTReader


logger = logging.getLogger(__name__)


class NeuralDataOriginator():
    def __init__(self, dataset, metadata, use_htk=False):
        self.dataset = dataset      # this should have all relavant paths
        self.metadata = metadata    # this should have all relevant metadata

        if use_htk:
            logger.info('Using HTK')
            self.neural_data_reader = HTKReader(self.dataset.htk_path)
        else:
            logger.info('Using TDT')
            self.neural_data_reader = TDTReader(self.dataset.tdt_path)

    def make(self, nwb_content, electrode_table_regions):
        for device_name, dev_conf in self.metadata['device'].items():
            if isinstance(dev_conf, str): # skip other annotations
                continue

            data, metadata = self.neural_data_reader.get_data(device_name, dev_conf)
            if data is None:
                logger.info(f'No data availble for {device_name}. Skipping...')
            else:
                electrode_table_region = electrode_table_regions[device_name]
                e_series = ElectricalSeries(name=device_name,
                                            data=data,
                                            electrodes=electrode_table_region,
                                            starting_time=0.,
                                            rate=metadata['sampling_rate'],
                                            )
                logger.info(f'Adding {device_name} data NWB...')
                nwb_content.add_acquisition(e_series)
