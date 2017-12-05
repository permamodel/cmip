"""tests subpackage for bmi_cmip

Provides:
    bmi_cmip_directory: the 'root' directory of the bmi_cmip module
    tests_directory: the directory containing the module's automated tests
    data_directory: the directory where installed data files are found
    examples_directory: the directory where installed data files are found
"""

import os

tests_directory = os.path.dirname(__file__)
bmi_cmip_directory = os.path.join(tests_directory, '..')
data_directory = os.path.join(bmi_cmip_directory, 'data')
examples_directory = os.path.join(bmi_cmip_directory, 'examples')

