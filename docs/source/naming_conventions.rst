.. nsds_lab_to_nwb

==================
Naming Conventions
==================

Animals

- ``RFLYY`` is ``R``\ at, surgeon's ``F``\ irst and ``L``\ ast initials, rat number (``YY``)
- ``BXX`` is ``B``\ lock number
- ``RYY`` are legacy animals

All blocks should be stored within an animal folder ``.../RFLYY/RFLYY_BXX``

Variable names

- ``XX_path`` indicates the full path to the folder or file
- ``XX_folder`` or ``XX_file`` should just be the folder or file name with no path
- ``block_folder`` is the full ``RFLYY_BXX``, ``block_name`` is ``BXX``, ``block_id`` is ``XX``
- ``animal_name`` should always be parsed from ``block_folder``, not manipulated separately or used as an argument

These arguments can have defaults set using environment variables

- ``data_path`` path to the top-level data folder. Should contain animal folders. Environment variable: ``NSDS_DATA_PATH``
- ``metadata_lib_path`` path to the metadata repo. Environment variable: ``NSDS_METADATA_PATH``
- ``stim_lib_path`` path to the stimulus folder. Environment variable: ``NSDS_STIMULI_PATH``

``nsds_lab_to_nwb.utils`` has utility functions for getting path defaults and parsing block folders.
