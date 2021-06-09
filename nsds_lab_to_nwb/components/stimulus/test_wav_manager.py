from nsds_lab_to_nwb.components.stimulus.wav_manager import WavManager

stim_path = '/run/user/1001/gvfs/smb-share:server=cadmus.lbl.gov,share=nselab/Stimulus'
stim_name = 'White noise' #I think this is wrong... not sure what to pass here

def test_wav_manager(stim_path, stim_name):
    wm = WavManager(stim_path, stim_name)
    #wm.get_stim_wav() not sure what first_mark is?
    wm.get_stim_file(stim_name, stim_path)

test_wav_manager(stim_path, stim_name)