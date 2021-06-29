import itertools


class ElectrodesOriginator():
    def __init__(self, metadata):
        self.metadata = metadata

    def make(self, nwb_content):
        device_electrode_regions = self.__add_electrodes(nwb_content)
        electrode_table_regions = self.__create_electrode_table_regions(nwb_content, device_electrode_regions)
        return electrode_table_regions

    def __add_electrodes(self, nwb_content):
        device_electrode_regions = {}
        e_id_gen = itertools.count()    # Electrode ID, unique for channels across devices
        for device_name in nwb_content.devices:
            # device = nwb_content.devices[device_name]
            e_group = nwb_content.electrode_groups[device_name]
            dev_config = self.metadata['device'][device_name]

            # Add each electrode
            electrode_region = []
            ch_ids = dev_config['ch_ids']
            ch_pos = dev_config['ch_pos']
            for i in ch_ids:
                e_id = next(e_id_gen)
                nwb_content.add_electrode(
                    id=e_id,
                    x=ch_pos[str(i)]['x'],
                    y=ch_pos[str(i)]['y'],
                    z=ch_pos[str(i)]['z'],
                    location=dev_config['location'],
                    imp=dev_config['imp'],
                    filtering=dev_config['filtering'],
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
