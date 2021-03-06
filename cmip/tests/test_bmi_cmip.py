"""
test_bmi_cmip.py
  tests of the bmip component of permamodel using bmi API
"""

import datetime
import os
import numpy as np

from nose.tools import assert_equal, assert_not_equal

import cmip
from cmip.tests import examples_directory

default_config_filename = os.path.join(examples_directory,
                                       'sample_cmip.cfg')

# ---------------------------------------------------
# Tests that ensure we have bmi functionality
# ---------------------------------------------------
def test_cmip_has_initialize():
    # Can we call an initialize function?
    ct = cmip.bmi_cmip.BmiCMIPComponentMethod()
    ct.initialize(cfg_file=default_config_filename)


def test_initialize_sets_times():
    # Can we call an initialize function?
    ct = cmip.bmi_cmip.BmiCMIPComponentMethod()
    ct.initialize(cfg_file=default_config_filename)
    assert_equal(ct._model.first_date, datetime.date(1902, 12, 15))


def test_att_map():
    ct = cmip.bmi_cmip.BmiCMIPComponentMethod()
    ct.initialize(cfg_file=default_config_filename)
    assert_equal('PermaModel_CMIPComponent', ct.get_attribute('model_name'))
    assert_equal('days', ct.get_attribute('time_units'))


def test_get_input_var_names():
    ct = cmip.bmi_cmip.BmiCMIPComponentMethod()
    ct.initialize(cfg_file=default_config_filename)
    input_vars = ct.get_input_var_names()
    # no input variables for cmip
    assert_equal(0, len(input_vars))


def test_get_output_var_names():
    ct = cmip.bmi_cmip.BmiCMIPComponentMethod()
    ct.initialize(cfg_file=default_config_filename)
    output_vars = ct.get_output_var_names()
    output_list = ('atmosphere_bottom_air__temperature',
                   'atmosphere_bottom_air__temperature_mean_jan',
                   'atmosphere_bottom_air__temperature_mean_jul',
                   'atmosphere_bottom_air__temperature_year')
    # In the future, we may include the start and end datetimes as outputs
    #output_list = ('atmosphere_bottom_air__temperature', 'datetime__start',
    #               'datetime__end')
    assert_equal(output_vars, output_list)


def test_get_var_name():
    ct = cmip.bmi_cmip.BmiCMIPComponentMethod()
    ct.initialize(cfg_file=default_config_filename)
    this_var_name = ct.get_var_name('atmosphere_bottom_air__temperature')
    assert_equal(this_var_name, 'T_air')
    this_var_name = \
        ct.get_var_name('atmosphere_bottom_air__temperature_mean_jul')
    assert_equal(this_var_name, 'T_air_jul')


def test_update_changes_temperature():
    b0 = cmip.bmi_cmip.BmiCMIPComponentMethod()

    b0.initialize(cfg_file=default_config_filename)

    index_flat = 350
    index2D = (10, 5)

    Tb0_2d_0 = b0.get_value(
        'atmosphere_bottom_air__temperature')[index2D]
    Tb0_flat_0 = b0.get_value(
        'atmosphere_bottom_air__temperature').flatten()[index_flat]

    Tb0_2d_last = 0.0
    Tb0_flat_last = 0.0
    for i in range(1, 11):
        b0.update()

        Tb0_2d = b0.get_value(
            'atmosphere_bottom_air__temperature')[index2D]
        Tb0_flat = b0.get_value(
            'atmosphere_bottom_air__temperature').flatten()[index_flat]

        assert_not_equal(Tb0_2d_last, Tb0_2d)
        assert_not_equal(Tb0_flat_last, Tb0_flat)

        Tb0_2d_last = Tb0_2d
        Tb0_flat_last = Tb0_flat
