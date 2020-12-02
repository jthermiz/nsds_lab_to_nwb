class TdtOriginator():
    def __init__(self, dataset, metadata):
        self.dataset = dataset      # this should have all relavant paths
        self.metadata = metadata    # this should have all relevant metadata

    def make(self, nwb_content):
        e_series = self.__create_electrical_series()
        nwb_content.add_acquisition(e_series)

    def __create_electrical_series(self):
        # extract and format
        pass
