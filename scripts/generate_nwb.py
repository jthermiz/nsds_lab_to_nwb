import os

from nsds_lab_to_nwb.nwb_builder import NWBBuilder
from nsds_lab_to_nwb.metadata.metadata_manager import MetadataManager

PWD = os.path.dirname(os.path.abspath(__file__))
USER_HOME = os.path.expanduser("~")

# --- user input and metadata for an experiment block ---

animal_name = 'R56'
block = 'B10'
# block = 'B13'

# raw data path
data_path = '/clusterfs/NSDS_data/hackathon20201201/'

# output path
out_path = os.path.join(USER_HOME, 'Data/nwb_test/')

# link to metadata files
block_metadata_path = os.path.join(PWD, f'../yaml/{animal_name}/{animal_name}_{block}.yaml')
library_path = os.path.join(USER_HOME, 'Src/NSDSLab-NWB-metadata/')


# --- collect metadata needed to build the NWB file ---

nwb_metadata = MetadataManager(block_metadata_path=block_metadata_path,
                               library_path=library_path)


# --- build NWB file for the specified block ---

# create a builder for the block
nwb_builder = NWBBuilder(
                animal_name=animal_name,
                block=block,
                data_path=data_path,
                out_path=out_path,
                nwb_metadata=nwb_metadata
                )

# build the NWB file content
nwb_content = nwb_builder.build()

# write to file
nwb_builder.write(nwb_content)
