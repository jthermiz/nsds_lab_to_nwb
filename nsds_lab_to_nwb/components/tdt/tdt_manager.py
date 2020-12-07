import tdt
import datetime as dt
from pynwb.ecephys import ElectricalSeries


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
                                    **add_other_fields_as_necessary
                                    )
        return e_series

    def __extract_from_tdt_files(self, device_name, dev_conf):
        tdt_path = self.tdt_path
        header = tdt.read_block(tdt_path, headers=1)
        num_channels = len(header.stores[device_name].chan)
        all_tdt_data = tdt.read_block(tdt_path) #I see no way to individually pull data streams using tdt's package, inefficent!
        data = all_tdt_data.streams[device_name].data.T
        # Iteratively write one channel at a time (TODO!)
        # data = DataChunkIterator(data=iter_tdt_channels(tdt_path, device_name, header, num_channels),
        #                          maxshape= (None, num_channels), 
        #                          buffer_size=BUFFER_SIZE) 
        tdt_params = {}
        tdt_params['start_time'] = dt.datetime.fromtimestamp(header.start_time[0]) #i think this is right (confirm timestamp is accurate with another dataset)
        tdt_params['stop_time'] = dt.datetime.fromtimestamp(header.stop_time[0])
        tdt_params['sample_rate'] = header.stores[device_name].fs
        return data, tdt_params
    
    def __iter_tdt_channels(self, device_name, header, num_channels):
        #This method does not work, but could be a starting point for implementing iterative write to nwb
        tdt_path = self.tdt_path
        for ch in range(num_channels):
            tdt_ch = ch + 1
            tdt_struct = tdt.read_block(tdt_path, 
                                        channel=tdt_ch, 
                                        #headers=header, 
                                        evtype=['streams'])
            ch_data = tdt_struct.streams[device_name].data
            print(ch_data.shape)
            yield ch_data
        return
        