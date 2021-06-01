import os

error_string = ("{} not set. Add 'export {}=/mypath/folder' "
                " to your .bashrc file or equivalent.")


def get_data_path(path=None):
    """Returns the path to the base NSDS data path. This path should contain the animal folder.

    Parameters
    ----------
    path : str
        Path to the stored data. If `None`, attempts to get the path from an environment varible.

    Returns
    -------
    path : str
        If availble, the path.
    """
    string = 'NSDS_DATA_PATH'
    if path is None:
        path = os.environ.get(string, None)
    if path is None:
        raise ValueError(error_string.format(string, string))
    return os.path.expanduser(path)


def get_metadata_path(path=None):
    """Returns the path to the base NSDS metadata path. This path should be the repo folder
    from
    https://github.com/BouchardLab/NSDSLab-NWB-metadata

    Parameters
    ----------
    path : str
        Path to the metatdata folder. If `None`, attempts to get the path from an environment
        varible.

    Returns
    -------
    path : str
        If availble, the path.
    """
    string = 'NSDS_METADATA_PATH'
    if path is None:
        path = os.environ.get(string, None)
    if path is None:
        raise ValueError(error_string.format(string, string))
    return os.path.expanduser(path)


def get_stimuli_path(path=None):
    """Returns the path to the stimuli .wav files.

    Parameters
    ----------
    path : str
        Path to the stored data. If `None`, attempts to get the path from an environment varible.

    Returns
    -------
    path : str
        If availble, the path.
    """
    string = 'NSDS_STIMULI_PATH'
    if path is None:
        path = os.environ.get(string, None)
    if path is None:
        raise ValueError(error_string.format(string, string))
    return os.path.expanduser(path)
