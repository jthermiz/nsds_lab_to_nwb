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
        data = self.__extract_from_tdt_files(device_name, dev_conf)
        # starting_time = 0.0                   # should confirm
        # rate = dev_conf['sampling_rate']      # should confirm

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
        # return data
        raise NotImplementedError('TODO')
