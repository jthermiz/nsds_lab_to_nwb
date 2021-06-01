<<<<<<< HEAD
import logging.config
import os
=======
>>>>>>> 3ae99b3... initial path work
import argparse

from nsds_lab_to_nwb import get_data_path, get_metadata_path, get_stimuli_path
from nsds_lab_to_nwb.nwb_builder import NWBBuilder
from nsds_lab_to_nwb.metadata.metadata_manager import MetadataManager

parser = argparse.ArgumentParser(description='Convert to a NWB file.')
parser.add_argument('save_path', type=str)
parser.add_argument('block_name', type=str)
parser.add_argument('--data_path', '-d', type=str, default=None)
parser.add_argument('--metadata_path', '-m', type=str, default=None)
parser.add_argument('--stimuli_path', '-s', type=str, default=None)
parser.add_argument('--legacy_block', '-l', action='store_true')
parser.add_argument('--use_htk', '-h', action='store_true')

args = parser.parse_args()

PWD = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(PWD) + '/../nsds_lab_to_nwb/logging.conf', disable_existing_loggers=False)


# --- user input and metadata for an experiment block ---

save_path = args.save_path
block_name = args.block_name
data_path = get_data_path(args.data_path)
metadata_path = get_metadata_path(args.metadata_path)
stimuli_path = get_stimuli_path(args.metadata_path)
legacy_block = args.legacy_block
use_htk = args.use_htk
block, animal_name = block_name.split('_')

# --- collect metadata needed to build the NWB file ---

nwb_metadata = MetadataManager(
                    data_path=data_path,
                    block_name=block_name,
                    metadata_path=metadata_path,
                    legacy_block=legacy_block
                    )


# --- build NWB file for the specified block ---

# NOTE: metadata collection is now done in NWBBuilder.__init__()

# create a builder for the block
nwb_builder = NWBBuilder(
                animal_name=animal_name,
                block=block,
                data_path=data_path,
                save_path=save_path,
                nwb_metadata=nwb_metadata,
                use_htk=use_htk)

# build the NWB file content
nwb_content = nwb_builder.build()

# write to file
nwb_builder.write(nwb_content)
