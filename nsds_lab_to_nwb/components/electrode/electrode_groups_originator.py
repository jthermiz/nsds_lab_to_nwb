import numpy as np
import itertools

class ElectrodeGroupsOriginator():
    def __init__(self, metadata):
        self.metadata = metadata

    def make(self, nwb_content):
        ''' create electrode groups '''
        for device_name, device in nwb_content.devices.items():
            e_group = nwb_content.create_electrode_group(
                name=device_name,
                description='',     # --- TODO: specify in metadata
                location='',        # --- TODO: specify in metadata
                device=device)
