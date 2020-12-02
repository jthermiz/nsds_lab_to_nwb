import os

from nsds_lab_to_nwb.nwb_builder import NWBBuilder
from nsds_lab_to_nwb.metadata.metadata_manager import MetadataManager


# --- user input and metadata for an experiment block ---

# raw data path
data_path = '/clusterfs/NSDS_data/hackathon20201201/'
animal_name = 'R56'
block = 'B10'

# output path
home = os.path.expanduser("~")
out_path = os.path.join(home, 'Data/nwb_test/')

# link to metadata files
metadata_path = 'path/to/metadata.yaml' # **TODO**
nwb_metadata = MetadataManager(metadata_path=metadata_path)


# --- build NWB file for the specified block ---

# create a builder for the block
nwb_builder = NWBBuilder(
                data_path=data_path,
                animal_name=animal_name,
                block=block,
                nwb_metadata=nwb_metadata,
                out_path=out_path
                )

# build the NWB file content
nwb_content = nwb_builder.build()

# write to file
nwb_builder.write(nwb_content)
