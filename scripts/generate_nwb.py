import logging.config
import os
import argparse

from nsds_lab_to_nwb.nwb_builder import NWBBuilder
from nsds_lab_to_nwb.metadata.metadata_manager import MetadataManager

parser = argparse.ArgumentParser(description='Convert to a NWB file.')
parser.add_argument('data_path', type=str)
parser.add_argument('library_path', type=str)
parser.add_argument('yaml_path', type=str)
parser.add_argument('save_path', type=str)
parser.add_argument('animal_name', type=str)
parser.add_argument('block', type=str)

args = parser.parse_args()

PWD = os.path.dirname(os.path.abspath(__file__))
USER_HOME = os.path.expanduser("~")

logging.config.fileConfig(fname=str(PWD) + '/../nsds_lab_to_nwb/logging.conf', disable_existing_loggers=False)


# --- user input and metadata for an experiment block ---

data_path = args.data_path
library_path = args.library_path
yaml_path = args.yaml_path
save_path = args.save_path
animal_name = args.animal_name
block = args.block
block_name = '{}_{}'.format(animal_name, block)

# --- collect metadata needed to build the NWB file ---

nwb_metadata = MetadataManager(
                    block_name=block_name, # required for new pipeline
                    block_metadata_path=yaml_path,
                    library_path=library_path
                    )


# --- build NWB file for the specified block ---

# NOTE: metadata collection is now done in NWBBuilder.__init__()

# create a builder for the block
nwb_builder = NWBBuilder(
                animal_name=animal_name,
                block=block,
                data_path=data_path,
                out_path=save_path,
                nwb_metadata=nwb_metadata,
                use_htk=False)

# build the NWB file content
nwb_content = nwb_builder.build()

# write to file
nwb_builder.write(nwb_content)
