from pynwb import TimeSeries

from nsds_lab_to_nwb.components.htk.readers.htkfile import HTKFile
from nsds_lab_to_nwb.components.tdt.tdt_reader import TDTReader


class MarkManager():
    def __init__(self, dataset):
        self.dataset = dataset

    def get_mark_track(self, name='recorded_mark'):
        # Read the mark track
        if hasattr(self.dataset, 'htk_mark_path'):
            mark_file = HTKFile(self.dataset.htk_mark_path)
            mark_track, meta = mark_file.read_data()
            rate = mark_file.sample_rate
        else:
            mark_track, meta = TDTReader(self.dataset.tdt_path).get_data('mrk1')
            rate = meta['sample_rate']

        # Create the mark timeseries
        mark_time_series = TimeSeries(name=name,
                                      data=mark_track,
                                      unit='Volts',
                                      starting_time=0.0,
                                      rate=rate,
                                      description='The stimulus mark track.')
        return mark_time_series
