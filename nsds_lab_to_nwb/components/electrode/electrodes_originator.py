import itertools


class ElectrodesOriginator():
    def __init__(self, metadata):
        self.metadata = metadata

    def make(self, nwb_content):
        self.__create_devices(nwb_content)
        self.__create_electrode_groups(nwb_content)
        device_electrode_regions = self.__add_electrodes(nwb_content)
        electrode_table_regions = self.__create_electrode_table_regions(nwb_content, device_electrode_regions)
        return electrode_table_regions

    def __create_devices(self, nwb_content):
        ''' create devices '''
        for device_name, dev_conf in self.metadata['device'].items():
            if not isinstance(dev_conf, dict):
                # skip any extra items in metadata
                continue
            device = nwb_content.create_device(name=device_name,
                                               manufacturer=dev_conf['manufacturer'])

    def __create_electrode_groups(self, nwb_content):
        ''' create electrode groups '''
        for device_name, device in nwb_content.devices.items():
            # in our case, only one ElectrodeGroup per device;
            # therefore ElectrodeGroup name is the same as device name
            dev_conf = self.metadata['device'][device_name]
            e_group = nwb_content.create_electrode_group(
                name=device_name,
                description=dev_conf['description'],
                location=dev_conf['location'],
                device=device)

    def __add_electrodes(self, nwb_content):
        device_electrode_regions = {}
        e_id_gen = itertools.count()    # Electrode ID, unique for channels across devices
        for device_name in nwb_content.devices:
            e_group = nwb_content.electrode_groups[device_name]
            dev_conf = self.metadata['device'][device_name]

            # Add each electrode
            electrode_region = []
            ch_ids = dev_conf['ch_ids']
            ch_pos = dev_conf['ch_pos']
            for i in ch_ids:
                e_id = next(e_id_gen)
                nwb_content.add_electrode(
                    id=e_id,
                    x=ch_pos[str(i)]['x'],
                    y=ch_pos[str(i)]['y'],
                    z=ch_pos[str(i)]['z'],
                    location=dev_conf['location'],
                    imp=dev_conf['imp'],
                    filtering=dev_conf['filtering'],
                    group=e_group)
                # Collect device channel IDs for electrode table region
                electrode_region.append(e_id)
            device_electrode_regions[device_name] = electrode_region
        return device_electrode_regions

    def __create_electrode_table_regions(self, nwb_content, device_electrode_regions):
        e_regions = {}
        for device_name, electrode_region in device_electrode_regions.items():
            # Create the electrode table region for this device
            table_region = nwb_content.create_electrode_table_region(
                                region=electrode_region,
                                description=f'Electrode table region for device {device_name}')
            e_regions[device_name]=table_region
        return e_regions
