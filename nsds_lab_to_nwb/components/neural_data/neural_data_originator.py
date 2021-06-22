import logging.config

from pynwb.ecephys import ElectricalSeries
from nsds_lab_to_nwb.components.htk.htk_manager import HTKManager
from nsds_lab_to_nwb.components.tdt.tdt_manager import TDTManager
from process_nwb.resample import resample

logger = logging.getLogger(__name__)


class NeuralDataOriginator():
    def __init__(self, dataset, metadata, use_htk=False, resample_flag=True):
        self.dataset = dataset      # this should have all relavant paths
        self.metadata = metadata    # this should have all relevant metadata
        self.resample_flag = resample_flag  #whether to attempt to resample or not
        self.hardware_sample_rate = None

        if use_htk:
            logger.info('Using HTK')
            self.neural_data_manager = HTKManager(self.dataset.htk_path)
        else:
            logger.info('Using TDT')
            self.neural_data_manager = TDTManager(self.dataset.tdt_path)
            
    def add_es_description(self):        
        device_name = self.e_series.name
        hardware_sample_rate = self.hardware_sample_rate 
        description = self.metadata['experiment_description']
        description += ' Recordings from {0:s} sampled at {1:f} Hz'.format(device_name, 
                                                       hardware_sample_rate)
        if self.resample_flag:
            description += ' Resampled down to {0:d} Hz'.format(self.e_series.rate)
            
        self.e_series = ElectricalSeries(name=device_name, 
                                    data=self.e_series,
                                    electrodes=self.e_series.electrodes,
                                    rate=self.e_series.rate,
                                    starting_time=self.e_series.starting_time,
                                    resolution=self.e_series.resolution,
                                    #unit=self.e_series.unit, pynwb forces users to use 'volts'?
                                    comments=self.e_series.comments, 
                                    description=description)
        
    
    def resample_es(self):        
        #only resample if rate is not at nearest kHz
        if (self.e_series.rate/1000 % 1) > 0:
            old_freq = self.e_series.rate
            new_freq = (old_freq//1000)*1000            
            new_data = resample(self.e_series.data, new_freq, old_freq)
            self.e_series = ElectricalSeries(name=self.e_series.name, 
                                             data=new_data,
                                             electrodes=self.e_series.electrodes,
                                             rate=new_freq,
                                             starting_time=self.e_series.starting_time,
                                             resolution=self.e_series.resolution,
                                             #unit=self.e_series.unit, pynwb forces users to use 'volts'?
                                             comments=self.e_series.comments)


    def make(self, nwb_content, electrode_table_regions):
        for device_name, dev_conf in self.metadata['device'].items():
            if isinstance(dev_conf, str): # skip other annotations
                continue

            self.e_series = self.neural_data_manager.extract(device_name, dev_conf,
                                                        electrode_table_regions[device_name])
            self.hardware_sample_rate = self.e_series.rate
            
            # resample to nearest khz
            if self.resample_flag:
                self.resample_es()
                
            # add description
            self.add_es_description()      
            
            if self.e_series is None:
                logger.info('No e-series extracted. Skipping...')
            else:
                logger.info('Adding extracted e-series to NWB...')
                nwb_content.add_acquisition(self.e_series)
