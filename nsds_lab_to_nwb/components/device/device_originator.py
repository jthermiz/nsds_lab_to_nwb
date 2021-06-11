class DeviceOriginator():
    def __init__(self, metadata):
        self.metadata = metadata

    def make(self, nwb_content):
        ''' create devices '''
        for device_name, dev_conf in self.metadata['device'].items():
            if isinstance(dev_conf, str): #Skip mark and audio,
                continue
            device = nwb_content.create_device(name=device_name,
                                               manufacturer=dev_conf['manufacturer'])
