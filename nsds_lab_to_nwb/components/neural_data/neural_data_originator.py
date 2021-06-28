import logging.config
from pynwb.ecephys import ElectricalSeries

from nsds_lab_to_nwb.components.htk.htk_reader import HTKReader
from nsds_lab_to_nwb.components.tdt.tdt_reader import TDTReader
from process_nwb.resample import resample

logger = logging.getLogger(__name__)


class NeuralDataOriginator():
    def __init__(self, dataset, metadata, resample_flag=True):
        self.dataset = dataset      # this should have all relavant paths
        self.metadata = metadata    # this should have all relevant metadata
        self.resample_flag = resample_flag
        self.hardware_rate = None
        self.resample_rate = None

        if hasattr(self.dataset, 'htk_mark_path'):
            logger.info('Using HTK')
            self.neural_data_reader = HTKReader(self.dataset.htk_path)
        else:
            logger.info('Using TDT')
            self.neural_data_reader = TDTReader(self.dataset.tdt_path)

    def make_description(self, device_name):
        description = self.metadata['experiment_description']
        description += '. Recordings from {0:s} sampled at {1:f} Hz.'.format(device_name,
                                                                             self.hardware_rate)
        if self.resample_flag:
            description += ' Then resampled down to {0:d} Hz'.format(int(self.resample_rate))
        return description

    def resample(self, data):
        # only resample if rate is not at nearest kHz
        rate = self.hardware_rate
        if (rate / 1000 % 1) > 0:
            new_freq = (rate // 1000) * 1000
            new_data = resample(data, new_freq, rate)
            self.resample_rate = new_freq
            return new_data
        else:
            # no need to resample, already at nearest kHz
            self.resample_flag = False
            return data

    def _get_rate(self):
        if self.resample_rate is None:
            rate = self.hardware_rate
        else:
            rate = self.resample_rate
        return rate * 1.0

    def make(self, nwb_content, electrode_table_regions):
        for device_name, dev_conf in self.metadata['device'].items():
            if isinstance(dev_conf, str): # skip other annotations
                continue

            data, metadata = self.neural_data_reader.get_data(stream=device_name, dev_conf=dev_conf)
            if data is None:
                logger.info(f'No data availble for {device_name}. Skipping...')
            else:

                # resample data
                self.hardware_rate = metadata['sample_rate']
                if self.resample_flag:
                    data = self.resample(data)

                # make description
                description = self.make_description(device_name)

                electrode_table_region = electrode_table_regions[device_name]
                e_series = ElectricalSeries(name=device_name,
                                            data=data,
                                            electrodes=electrode_table_region,
                                            starting_time=0.,
                                            rate=self._get_rate(),
                                            description=description
                                            )
                logger.info(f'Adding {device_name} data NWB...')
                nwb_content.add_acquisition(e_series)
