from nsds_lab_to_nwb.components.htk.readers.htkfile import HTKFile

class HtkReader():
    def __init__(self):
        pass

    @staticmethod
    def read_htk(path):
        file = HTKFile(path)
        data = file.read_data()
        return data, file.sample_rate
