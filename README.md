# NSDS_lab_to_NWB

Python code package to convert NSDS lab data to NWB files.

Under development - anything could change.

Metadata library is in a separate repository [NSDSLab-NWB-metadata](https://github.com/BouchardLab/NSDSLab-NWB-metadata) (private to BouchardLab).


## Setup

Clone this repository and `cd` to the repository root:

```bash
cd [your_project_folder]
git clone git@github.com:BouchardLab/nsds_lab_to_nwb.git
cd nsds_lab_to_nwb
```

Create a conda environment:

```bash
conda env create -f environment.yml
```

Also install this package:

```bash
pip install -e .
```

Some test scripts also assume that you have cloned the metadata repository:
(Bouchard lab internal access only)

```bash
mkdir -p ~/Src
cd ~/Src
git clone git@github.com:BouchardLab/NSDSLab-NWB-metadata.git
```
