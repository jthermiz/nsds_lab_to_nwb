import logging.config

from nsds_lab_to_nwb.components.htk.readers.instrument import EPhysInstrumentData

logger = logging.getLogger(__name__)


class HTKReader:
    """HTK interface

    Parameters
    ----------
    path: str
        Path to HTK folder
    channels: list, optional
        List of channel ids to import. Defaults to None.
    """
    def __init__(self, path, channels=None):
        self.path = path

    def get_data(self, *, stream=None, dev_conf=None):
        """Get specified data

        Parameters
        ----------
        stream: str
            Stream name (not used by HTKReader)
        dev_conf: (dict) metadata for the device.
            nwb_builder.metadata['device'][device_name]. Not used for TDT.

        Returns
        -------
        data: ndarray
            Data array
        meta: dict
            Meta data for the data array.
        """
        device_reader = EPhysInstrumentData(
            htkdir=self.path,
            prefix=dev_conf['prefix'],
            postfix=dev_conf['ch_ids'],
            device_name=dev_conf['device_type'],
            read_on_create=False)
        device_reader.read_data(create_iterator=True, time_axis_first=True, has_bands=False)

        data = device_reader.data
        meta = {}
        meta['sample_rate'] = device_reader.sample_rate
        return data, meta
