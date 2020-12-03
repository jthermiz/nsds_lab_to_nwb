from pynwb import TimeSeries

from nsds_lab_to_nwb.components.htk.htk_reader import HtkReader


class MarkManager():
    def __init__(self, mark_path):
        self.mark_path = mark_path


    def get_mark_track(self, name='recorded_mark'):
        # Read the mark track
        mark_track, rate = HtkReader.read_htk(self.mark_path)

        # Create the mark timeseries
        mark_time_series = TimeSeries(name=name,
                            data=mark_track,
                            unit='Volts',
                            starting_time=0.0,
                            rate=rate,
                            description='The neural recording aligned stimulus mark track.')
        return mark_time_series
