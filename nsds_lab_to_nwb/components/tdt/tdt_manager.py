import tdt
import numpy as np
from pynwb.ecephys import ElectricalSeries
from hdmf.data_utils import DataChunkIterator

BUFFER_SIZE = 32 #Buffer these many channels into a chunk

class TdtManager():
    def __init__(self, tdt_path):
        self.tdt_path = tdt_path

    def extract_tdt(self, device_name, dev_conf, electrode_table_region):
        '''
        extracts TDT data for a single device, and returns an ElectricalSeries.
        
        Args:
        - device_name: (str) either 'ECoG' or 'Poly'
        - dev_conf: (dict) metadata for the device.
                           nwb_builder.metadata['device'][device_name]
        - electrode_table_region: NWB electrode table region for the device
        Returns:
        - e_series: (ElectricalSeries) to be added to the NWB file
        '''
        data, tdt_params = self.__extract_from_tdt_files(device_name, dev_conf)
        starting_time = tdt_params['start_time']
        rate = tdt_params['sample_rate']

        # Create the electrical series
        e_series = ElectricalSeries(name=device_name,
                                    data=data,
                                    electrodes=electrode_table_region,
                                    starting_time=starting_time,
                                    rate=rate,
                                    # **add_other_fields_as_necessary
                                    )
        return e_series
    
    def __iter_tdt_channels(self, tdt_path, stream, header, num_channels):
        #this is inefficient because it loads all streams. As far as I can tell,
        #there's no way to select streams to load
        for ch in range(num_channels):
            tdt_ch = ch + 1
            tdt_struct = tdt.read_block(tdt_path, 
                                        channel=tdt_ch, 
                                        headers=header, 
                                        evtype=['streams'])
            ch_data = tdt_struct.streams[stream].data
            ch_data = np.reshape(1, -1) #weird quirk to make data samples x channels since it's tranposed downstream
            yield ch_data
        return

    def __extract_from_tdt_files(self, device_name, dev_conf):
        tdt_path = self.tdt_path
        header = tdt.read_block(tdt_path, headers=1)
        tdt_tmp = tdt.read_block(tdt_path, channel=1)
        num_channels = len(header.stores[device_name].chan)
        num_samples = len(tdt_tmp.streams[device_name].data)
        # Iteratively write one channel at a time 
        data = DataChunkIterator(data=self.__iter_tdt_channels(tdt_path, device_name, header, num_channels),
                                  maxshape= (num_samples, num_channels), 
                                  buffer_size=BUFFER_SIZE) 
        tdt_params = {}
        tdt_params['start_time'] = header.start_time[0] #returning numeric since that's what nwb wants for an eseries
        tdt_params['stop_time']  = header.stop_time[0]
        #tdt_params['stop_time'] = dt.datetime.fromtimestamp(header.stop_time[0])
        tdt_params['sample_rate'] = header.stores[device_name].fs
        return data, tdt_params   

    

        