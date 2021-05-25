import tdt
import numpy as np
import warnings
import sys
from nsds_lab_to_nwb.components.tdt.tdt_reader import TDTReader
from pynwb.ecephys import ElectricalSeries
from hdmf.data_utils import DataChunkIterator

class TdtManager(TDTReader):    
    def extract_tdt(self, device_name, dev_conf, electrode_table_region):
        '''
        extracts TDT data for a single device, and returns an ElectricalSeries.

        Args:
        - device_name: (str) either 'Wave' or 'Poly'
        - dev_conf: (dict) metadata for the device.
                           nwb_builder.metadata['device'][device_name]
        - electrode_table_region: NWB electrode table region for the device
        Returns:
        - e_series: (ElectricalSeries) to be added to the NWB file
        '''
        if device_name not in self.streams:
            error_message = 'Device or stream not found. Available streams: '
            for stream in self.streams:
                error_message += stream + ', '
            warnings.warn(error_message)
            return None

        data, tdt_params = self.get_data(device_name)
        data = data.T #tranpose to long form matrix
        rate = tdt_params['sample_rate']

        # Create the electrical series
        e_series = ElectricalSeries(name=device_name,
                                    data=data,
                                    electrodes=electrode_table_region,
                                    starting_time=0.,
                                    rate=rate,
                                    # **add_other_fields_as_necessary
                                    )
        return e_series
