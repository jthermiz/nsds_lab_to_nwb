import logging.config
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

from nsds_lab_to_nwb.metadata.metadata_manager import MetadataManager


path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + 'logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NWBBuilder:
    '''Unpack data from a specified block, and write those data into NWB file format.
    '''

    def __init__(
            self,
            data_path: str,
            animal_name: str,
            block: str,
            nwb_metadata: MetadataManager,
            out_path: str = ''
    ):
        self.data_path = data_path
        self.animal_name = animal_name
        self.block = block
        self.metadata = nwb_metadata.metadata
        self.out_path = out_path
        
        self.output_file = os.path.join(self.out_path,
                                self.animal_name + '_' + self.block + '.nwb')

    def build(self):
        '''Build NWB file content.
        '''
        logger.info('Building components for NWB')
        nwb_content = NWBFile(
            session_description=self.metadata['session description'],
            experimenter=self.metadata['experimenter name'],
            lab=self.metadata['lab'],
            institution=self.metadata['institution'],
            identifier=str(uuid.uuid1()),
            session_id=self.metadata['session_id'],
            experiment_description=self.metadata['experiment description'],
            subject=Subject(
                subject_id=self.metadata['subject']['subject id'],
                description=self.metadata['subject']['description'],
                genotype=self.metadata['subject']['genotype'],
                sex=self.metadata['subject']['sex'],
                species=self.metadata['subject']['species']
            ),
        )

        return nwb_content

    def write(self, content):
        '''Write collected NWB content into an actual file.
        '''

        logger.info('Writing down content to ' + self.output_file)
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()

        logger.info(self.output_file + ' file has been created.')
        return self.output_file
