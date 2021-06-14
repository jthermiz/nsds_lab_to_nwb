.. nsds_lab_to_nwb

============
Installation
============

Install from source
-------------------

The latest development version of the code can be installed from https://github.com/BouchardLab/nsds_lab_to_nwb

By design, these installation instructions will create a new conda environment names `nsds_nwb`
with all of the requirements satisfied.

.. code-block:: bash

    # use ssh
    $ git clone git@github.com:BouchardLab/nsds_lab_to_nwb.git
    # or use https
    $ git clone https://github.com/BouchardLab/nsds_lab_to_nwb.git
    $ cd nsds_lab_to_nwb
    $ conda env create -f environment.yml
    $ pip install -e .
