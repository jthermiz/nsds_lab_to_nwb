from nsds_lab_to_nwb.components.stimulus.mark_manager import MarkManager
from nsds_lab_to_nwb.components.stimulus.mark_tokenizer import MarkTokenizer
from nsds_lab_to_nwb.components.stimulus.wav_manager import WavManager


class StimulusOriginator():
    def __init__(self, dataset, metadata):
        self.dataset = dataset
        self.metadata = metadata
        self.stim_configs = self.metadata['stimulus']

        self.mark_manager = MarkManager(self.dataset)
        self.mark_tokenizer = MarkTokenizer(self.metadata['block_name'],
                                            self.stim_configs)

        self.wav_manager = WavManager(self.dataset.stim_lib_path,
                                      self.stim_configs)

    def make(self, nwb_content):
        # add mark track
        mark_starting_time = 0.0    # <<<< legacy behavior. confirm! always at 0.0?
        mark_time_series = self.mark_manager.get_mark_track(starting_time=mark_starting_time)
        nwb_content.add_stimulus(mark_time_series)

        # tokenize into trials, once mark track has been added to nwb_content
        self.mark_tokenizer.tokenize(nwb_content)

        # add stimulus WAV data
        stim_starting_time = self._get_stim_starting_time(nwb_content)
        stim_wav_time_series = self.wav_manager.get_stim_wav(starting_time=stim_starting_time)
        nwb_content.add_stimulus(stim_wav_time_series)

    def _get_stim_starting_time(self, nwb_content):
        if self.mark_tokenizer.tokenizable:
            time_table = nwb_content.trials.to_dataframe().query('sb == "s"')['start_time']
            # first_recorded_mark = time_table[1]  # <<< this was MARS version; legacy from matlab code?
            first_recorded_mark = time_table.values[0]
        else:
            # continuous stimulus
            first_recorded_mark = 0.0    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< just a guess. confirm!!!

        # starting time for the stimulus TimeSeries
        stim_starting_time = (first_recorded_mark
                         - self.stim_configs['mark_offset']  # adjust for mark offset
                         - self.stim_configs['first_mark'])  # time between stimulus DVD start and the first mark
        return stim_starting_time
