"""
test_cmip.py
  tests of the cmip component of permamodel
"""

import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
from nose.tools import (assert_almost_equal, assert_equal)
import cmip
import os


# ---------------------------------------------------
# Tests that the frost_number module is importing
# ---------------------------------------------------
def test_can_initialize_cmip_class():
    ct = cmip.cmip_model.CMIPComponentMethod
    assert ct is not None


def test_write_gridfile():
    """ Test that can write a gridfile to disk """
    # Create a temperature grid with default structure
    grid_desc = cmip.cmip_utils.write_gridfile('temperature')
    assert grid_desc is not None

    # Create a temperature grid with described shape and type
    grid_desc = cmip.cmip_utils.write_gridfile('temperature',
                                               gridshape=(3, 4),
                                               gridtype=np.float64)

    # Fail when attempting to create a grid with non-shape shape
    try:
        grid_desc = cmip.cmip_utils.write_gridfile('temperature',
                                                   gridshape='notashape')
    except ValueError:
        pass


def test_write_default_cfg_file():
    """ test that util operation writes default cfg file """
    default_cfg_filename = 'default_cmip.cfg'
    if os.path.isfile(default_cfg_filename):
        print('default config filename already exists, skipping test')
        print('  {}'.format(default_cfg_filename))
    else:
        cmip.cmip_utils.generate_default_cmip_cfg_file(\
            SILENT=True)
        os.remove(default_cfg_filename)


def test_initialize_opens_default_config_file():
    """ Test that temperature netcdf file is opened """
    ct = cmip.cmip_model.CMIPComponentMethod()
    ct.initialize_from_config_file()


def test_get_timestep_from_date():
    """ Test get timestep from a date """
    ct = cmip.cmip_model.CMIPComponentMethod()
    ct.initialize_from_config_file()

    # Timestep should initialize to zero
    this_timestep = 0
    assert_equal(this_timestep, ct._current_timestep)

    # Adding 10 years should make the current timestep 10
    number_of_years = 10
    ct.increment_date(number_of_years)
    assert_equal(10, ct._current_timestep)

    #...and make the date 10 days later
    this_timedelta = relativedelta(years=number_of_years)
    assert_equal(ct.first_date+this_timedelta, ct._current_date)


def test_time_index_yields_correct_values():
    """ Check that we get the expected index into the netcdf file
        for specified month and year """
    ct = cmip.cmip_model.CMIPComponentMethod()
    ct.initialize_from_config_file()

    # Test that first month yields index zero
    month = 1
    year = 1901
    idx = ct.get_time_index(month, year)
    assert_equal(idx, 0)

    # Test that a year later yields index 12
    month = 1
    year = 1902
    idx = ct.get_time_index(month, year)
    assert_equal(idx, 12)

    # Test that a century and a year later yields index 1212
    month = 1
    year = 2002
    idx = ct.get_time_index(month, year)
    assert_equal(idx, 1212)


def test_specific_netcdf_values():
    """ Test that indexing yields specific values chosen from file
        Values were hand-verified using panoply tables

        Note: this test could be skipped if underlying testing netcdf
        files aren't as expected
        """
    ct = cmip.cmip_model.CMIPComponentMethod()
    ct.initialize_from_config_file()

    # For Dec 1902, local grid (10, 13) is ncfile grid (45, 312)
    t_idx = 0
    x_idx = 11
    y_idx = 0
    #assert_almost_equal(ct._temperature[t_idx, y_idx, x_idx], 259.1304, places=2)
    assert_almost_equal(
        ct._temperature[t_idx, y_idx, x_idx], 260.1971, places=2)

    t_idx = 0
    x_idx = 3
    y_idx = 18
    assert_almost_equal(
        ct._temperature[t_idx, y_idx, x_idx], 252.3327, places=2)


def test_getting_monthly_annual_temp_values():
    """ Test that prior_months and prior_year values are correct
        Values were hand-verified using panoply tables"""
    ct = cmip.cmip_model.CMIPComponentMethod()
    ct.initialize_from_config_file()

    x_idx = 2
    y_idx = 1
    assert_almost_equal(ct.T_air_annual_mean[y_idx, x_idx], 271.7334, places=2)

    t_idx = 6
    x_idx = 19
    y_idx = 3
    jul_temperatures = ct.get_temperature_month_year(7, 1902)
    assert_almost_equal(jul_temperatures[y_idx, x_idx], 287.3322, places=2)


def test_can_increment_to_end_of_run():
    """ Test that we can get values for last timestep """
    ct = cmip.cmip_model.CMIPComponentMethod()
    ct.initialize_from_config_file()

    number_of_years = ct._last_timestep - ct._first_timestep
    ct.increment_date(number_of_years)
    ct.update_temperature_values()


def test_first_and_last_valid_dates():
    """ Test that first and last valid dates are read from netcdf file """
    ct = cmip.cmip_model.CMIPComponentMethod()
    ct.initialize_from_config_file()
    assert_equal(datetime.date(1901, 1, 1), ct._first_valid_date)
    assert_equal(datetime.date(2100, 12, 31), ct._last_valid_date)


def test_can_get_netcdf_filename_from_date():
    """ Test get correct filename for netcdf file """
    ct = cmip.cmip_model.CMIPComponentMethod()
    cfg = cmip.cmip_utils.generate_default_cmip_cfg_data()
    ct.initialize_from_config_struct(cfg)

    testdate = datetime.date(1910, 12, 25)
    fn = ct.get_current_ncdata_filename(testdate)

    dirname = cfg['srcdata_dir']
    filename_cfg = cfg['filepattern']
    filename_cfg = filename_cfg.replace('SRCDIR', dirname)
    filename_cfg = filename_cfg.replace('YEAR', '{:4d}'.format(testdate.year))

    assert_equal(filename_cfg, fn)


def test_can_get_subarray_for_date():
    """ for a given date verify we get monthly temp and precip """

    # NOTE: should check for valid values
    test_temp_field_file = './cmip/examples/CMIP_temperature_191012_test.dat'
    if not os.path.isfile(test_temp_field_file):
        print('Skipping test because test file does not exist:\n')
        print('  {}'.format(test_temp_field_file))
        return

    ct = cmip.cmip_model.CMIPComponentMethod()
    cfg = cmip.cmip_utils.generate_default_cmip_cfg_data()
    ct.initialize_from_config_struct(cfg)

    testdate = datetime.date(1910, 12, 25)

    # Configuration will set array bounds, and offset
    # Should assert the parameters here so as to check "correct" values

    temperature_array = ct.get_temperature_month_year(testdate.month,
                                                       testdate.year)

    # This should be from the 'testing' or 'examples' or 'data' directory?
    expected_temperature_array = \
        np.fromfile(test_temp_field_file, dtype=np.float32)
