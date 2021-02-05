import os

from nsds_lab_to_nwb.nwb_builder import NWBBuilder
from nsds_lab_to_nwb.metadata.metadata_manager import MetadataManager

path = os.path.dirname(os.path.abspath(__file__))


# --- user input and metadata for an experiment block ---

animal_name = 'R56'
block = 'B10'
# block = 'B13'

# raw data path
data_path = '/clusterfs/NSDS_data/hackathon20201201/'

# output path
home = os.path.expanduser("~")
out_path = os.path.join(home, 'Data/nwb_test/')

# link to metadata files
metadata_path = os.path.join(path, '../yaml/{}_{}.yaml'.format(animal_name, block))
library_path = os.path.join(home, 'Src/NSDSLab-NWB-metadata/')
nwb_metadata = MetadataManager(metadata_path=metadata_path,
                               library_path=library_path)


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
# nwb_content = nwb_builder.build(use_htk=True) # for testing non-TDT features

# write to file
nwb_builder.write(nwb_content)
