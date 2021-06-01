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


def split_block_folder(block_folder):
    """Splits the block_folder (`RFLYY_BXX`) into the surgeon initials (`FL`),
    animal_id `YY`, and block_id `XX`. For legacy blocks (`RFLYY_BXX`), surgeon initals is `None`.

    Parameters
    ----------
    block_folder : str
        Name of the folder.

    Returns
    -------
    surgeon_initials : str
        First and last name initials of the surgeon. (`None` for legacy blocks)
    animal_name : str
        Animal name. Should be the same as the folder that contains `block_folder`
    block_name : str
        Name of the block "B<block_id>".
    """
    if block_folder.count('_') != 1:
        raise ValueError("'block_folder' should contain only 1 '_'")
    if block_folder.count('/') > 0:
        raise ValueError("'block_folder' should be the block folder name, not the entire path.")
    surgeon_initials = block_folder[1:3]
    if not surgeon_initials.isalpha():
        surgeon_initials = None
        animal_id, block_id = block_folder.split('_')
        animal_id = animal_id[1:]
        block_id = block_id[1:]
    else:
        animal_id, block_id = block_folder.split('_')
        animal_id = animal_id[3:]
        block_id = block_id[1:]
        if not surgeon_initials.isalpha():
            raise ValueError(f"`surgeon_initials` is not a alpha string for {block_folder}")
    if not animal_id.isnumeric():
        raise ValueError(f"`animal_id` is not a numeric string for {block_folder}")
    if not block_id.isnumeric():
        raise ValueError(f"`block_id` is not a numeric string for {block_folder}")
    if surgeon_initials is None:
        animal_name = f"R{animal_id}"
    else:
        animal_name = f"R{surgeon_initials}{animal_id}"
    return surgeon_initials, animal_name, f"B{block_id}"
