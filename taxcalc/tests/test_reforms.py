"""
Tests all the example JSON parameter files located in taxcalc/reforms directory
      and all the JSON parameter files located in taxcalc/taxbrain directory
"""
# CODING-STYLE CHECKS:
# pep8 --ignore=E402 test_reforms.py
# pylint --disable=locally-disabled test_reforms.py
# (when importing numpy, add "--extension-pkg-whitelist=numpy" pylint option)

import os
import glob
import pytest
# pylint: disable=import-error
from taxcalc import Calculator, Policy, Behavior, Consumption, Growth


@pytest.fixture(scope='session')
def reforms_path(tests_path):
    """
    Return path to taxcalc/reforms/*.txt files
    """
    return os.path.join(tests_path, '..', 'reforms', '*.txt')


def test_reforms(reforms_path):  # pylint: disable=redefined-outer-name
    """
    Check that each JSON reform file can be converted into a reform dictionary
    that can then be passed to the Policy class implement_reform() method.
    While doing this, construct a set of Policy parameters (other than those
    ending in '_cpi') included in the JSON reform files.
    """
    params_set = set()
    for jrf in glob.glob(reforms_path):
        # read contents of jrf (JSON reform filename)
        with open(jrf) as jrfile:
            jrf_text = jrfile.read()
        # check that jrf_text has "policy" that can be implemented as a reform
        policy_dict = Calculator.read_json_policy_reform_text(jrf_text)
        policy = Policy()
        policy.implement_reform(policy_dict)
        # identify "policy" parameters included in jrf
        for year in policy_dict.keys():
            if year == 0:
                continue  # skip param_code info which is marked with year zero
            policy_year_dict = policy_dict[year]
            for param in policy_year_dict.keys():
                if param.endswith('_cpi'):
                    continue  # skip "policy" parameters ending in _cpi
                params_set.add(param)
    # TODO: compare params_set to set of parameters in current_law_policy.json
    assert len(params_set) > 0


@pytest.fixture(scope='session')
def taxbrain_path(tests_path):
    """
    Return path to taxcalc/taxbrain/*.json files
    """
    return os.path.join(tests_path, '..', 'taxbrain', '*.json')


def test_taxbrain_json(taxbrain_path):  # pylint: disable=redefined-outer-name
    """
    Check that each JSON parameter file can be converted into dictionaries
    that can be used to construct objects needed for a Calculator object.
    """
    for jpf in glob.glob(taxbrain_path):
        # read contents of jpf (JSON parameter filename)
        with open(jpf) as jpfile:
            jpf_text = jpfile.read()
        # check that jpf_text can be used to instantiate Calculator object
        if '"policy"' in jpf_text:
            pol = Calculator.read_json_policy_reform_text(jpf_text)
            policy = Policy()
            policy.implement_reform(pol)
        elif ('"behavior"' in jpf_text and
              '"consumption"' in jpf_text and
              '"growth"' in jpf_text):
            beh, con, gro = Calculator.read_json_econ_assump_text(jpf_text)
            behv = Behavior()
            behv.update_behavior(beh)
            cons = Consumption()
            cons.update_consumption(con)
            grow = Growth()
            grow.update_growth(gro)
        else:  # jpf_text is not a valid JSON parameter file
            assert False
