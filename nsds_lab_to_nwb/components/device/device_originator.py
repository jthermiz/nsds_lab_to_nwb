class DeviceOriginator():
    def __init__(self, metadata):
        self.metadata = metadata

    def make(self, nwb_content):
        ''' create devices '''
        for device_name, dev_conf in self.metadata['device'].items():
            if isinstance(dev_conf, str): #Skip mark and audio,
                continue
            device_source = dev_conf['manufacturer']
            device = nwb_content.create_device(name=device_name, 
                                            #source=device_source
                                            )
