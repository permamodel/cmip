"""cruAKtemp_utils.py

Utility routines for the cruAKtemp package
"""
import datetime
import errno
import os
import sys
import yaml
import numpy as np

def write_gridfile(gridname, gridshape=(1,), gridtype=np.float, filename=None):
    """write_grid: Creates a grid for permamodel runs
    gridshape: the dimensions of the grid array [default is a single point]
    gridtype:  the data type of the grid [default 4-byte floats]
    filename:  the file to write the yaml description to [default None
                 which means return the description
    """
    # Ensure that the grid description is legal
    try:
        tempgrid = np.zeros(gridshape, dtype=gridtype)
        assert tempgrid is not None
    except:
        raise ValueError("Can't create grid of shape %s and type %s: %s"\
                         % (str(gridshape), str(gridtype), sys.exc_info()[0]))
    griddict = {}
    griddict['gridname'] = gridname
    griddict['gridshape'] = gridshape
    griddict['gridtype'] = gridtype

    # Write the grid description to the provided filename or return it
    try:
        yamlstream = file(filename, 'w')
        yaml.dump(griddict, yamlstream)
        return None
    except TypeError:
        return yaml.dump(griddict)


def generate_default_cmip_cfg_data():
    # Generate the data for a default CMIP initialization
    # Description of model run
    cfgdict = {}

    cfgdict['run_description'] = "Sample Permafrost data...simulated CMIP"
    cfgdict['run_region'] = "Sample Permafrost region"

    # Grid description
    cfgdict['grid_type'] = 'rectilinear'
    #cfgdict['grid_shape'] = (5, 4)
    #cfgdict['i_ul'] = 25
    #cfgdict['j_ul'] = 317
    cfgdict['grid_shape'] = (40, 23)
    cfgdict['i_ul'] = 25
    cfgdict['j_ul'] = 299

    # Time description
    cfgdict['timestep'] = datetime.timedelta(days=1)
    #cfgdict['reference_date'] = datetime.date(1900, 1, 1)
    cfgdict['reference_date'] = datetime.datetime(1900, 1, 1)
    cfgdict['first_valid_year'] = 1901
    cfgdict['last_valid_year'] = 1910
    cfgdict['model_start_year'] = 1902
    cfgdict['model_end_year'] = 1910

    # The files to use to get information have the form of 'filepattern'
    cfgdict['srcdata_dir'] = '/data/SiB_PCF85'
    cfgdict['filepattern'] = 'SRCDIR/SiB_PCF85_data.t12.YEAR.nc'
    cfgdict['data_gridnames'] = {
        'temperature': 'TS',
        'precipitation': 'LSP'
        }
    cfgdict['grid_dtypes'] = {
        'temperature': 'np.float32',
        'precipitation': 'np.float32'
        }

    return cfgdict


def generate_default_cmip_cfg_file(filename=None,
                                   overwrite=False, SILENT=True):
    '''
    generate_default_cmip_cfg_file:
    Creates a default configuration file for bmi_cmip
    '''

    # The cfgdict dictionary stores the information about this configuration
    #cfgdict = {}
    cfgdict = generate_default_cmip_cfg_data()

    if filename is None:
        filename = 'default_cmip.cfg'
    cfgdict['filename'] = filename

    if overwrite:
        try:
            yamlfile = open(filename, 'w')
            yaml.dump(cfgdict, yamlfile)
            return None
        except:
            raise RuntimeError(\
                "Error trying to create default cmip cfg file: %s" \
                            % sys.exc_info[0])
    else:
        fileflags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            yamlfile_handle = os.open(filename, fileflags)
        except OSError as e:
            if e.errno == errno.EEXIST:
                if not SILENT:
                    print "config file exists, not overwritten: %s" % filename
                else:
                    pass
            else:
                raise
        else:
            with os.fdopen(yamlfile_handle, 'w') as yamlfile:
                yaml.dump(cfgdict, yamlfile)
            return None

