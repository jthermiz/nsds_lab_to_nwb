from nsds_lab_to_nwb.components.stimulus.mark_manager import MarkManager
from nsds_lab_to_nwb.components.stimulus.mark_tokenizer import MarkTokenizer
from nsds_lab_to_nwb.components.stimulus.wav_manager import WavManager


class StimulusOriginator():
    def __init__(self, dataset, metadata):
        self.dataset = dataset
        self.metadata = metadata

        self.mark_manager = MarkManager(self.dataset.mark_path)
        self.mark_tokenizer = MarkTokenizer(self.metadata['block_name'],
                                            self.metadata['stimulus'])

        self.wav_manager = WavManager(self.dataset.stim_path,
                                      self.metadata['stimulus'])

    def make(self, nwb_content):
        # add mark track
        mark_time_series = self.mark_manager.get_mark_track()
        nwb_content.add_stimulus(mark_time_series)

        # tokenize into trials, once mark track has been added to nwb_content
        self.mark_tokenizer.tokenize(nwb_content)

        # add stimulus WAV data
        first_recorded_mark = self.__get_first_recorded_mark(nwb_content)
        stim_wav_time_series = self.wav_manager.get_stim_wav(first_recorded_mark)
        nwb_content.add_stimulus(stim_wav_time_series)

    def __get_first_recorded_mark(self, nwb_content):
        time_table = nwb_content.trials.to_dataframe().query('sb == "s"')['start_time']
        # return time_table[1]  # <<< this was MARS version; legacy from matlab code?
        return time_table.values[0]
