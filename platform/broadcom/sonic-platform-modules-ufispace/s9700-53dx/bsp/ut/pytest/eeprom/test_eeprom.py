#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019 UfiSpace Co.,Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from bsp.utility.eeprom_utility import EEPRomUtility
from bsp.const.const import QSFP, QSFPDD
from bsp.utility.qsfp_utility import QSFPUtility
from bsp.utility.qsfpdd_utility import QSFPDDUtility

qsfp_ports = range(QSFP.MAX_PORT)
qsfpdd_ports = range(QSFPDD.MAX_PORT)

@pytest.fixture(scope="session")
def util():
    return EEPRomUtility()

@pytest.fixture(scope="session")
def qsfp_util():
    return QSFPUtility()

@pytest.fixture(scope="session")
def qsfpdd_util():
    return QSFPDDUtility()
    
def _compare_dict(dict_target, dict_expect):
    errors = []
    
    for key in dict_target.keys():        
        if dict_target[key] != dict_expect[key]:
            errors.append("{} is {}, expect {}".format(key, dict_target[key], dict_expect[key]))
    
    return errors

def test_dump_cpu_eeprom(util):
    output = util.dump_cpu_eeprom()    
    assert "content" in output

@pytest.mark.skip(reason="too long")
@pytest.mark.parametrize("port", qsfp_ports)
def test_dump_qsfp_eeprom(util, qsfp_util, port):    
    
    if (qsfp_util.get_presence(port)["presence"] != "presence"):
        pytest.skip("Module not present")
        
    output = util.dump_qsfp_eeprom(port)    
    assert "content" in output 

@pytest.mark.skip(reason="too long")
@pytest.mark.parametrize("port", qsfpdd_ports)
def test_dump_qsfpdd_eeprom(util, qsfpdd_util, port):    

    if (qsfpdd_util.get_presence(port)["presence"] != "presence"):
        pytest.skip("Module not present")
                
    output = util.dump_qsfpdd_eeprom(port)    
    assert "content" in output

@pytest.mark.parametrize("port", qsfp_ports)
def test_get_qsfp_info(util, qsfp_util, port):    

    if (qsfp_util.get_presence(port)["presence"] != "presence"):
        pytest.skip("Module not present")
         
    output = util.get_qsfp_info(port)    
    assert all (k in output for k in ("vendor","rx_pwr", "temp", "sn", "volt", "tx_bias"))

@pytest.mark.parametrize("port", qsfpdd_ports)
def test_get_qsfpdd_info(util, qsfpdd_util, port):
        
    if (qsfpdd_util.get_presence(port)["presence"] != "presence"):
        pytest.skip("Module not present")
        
    output = util.get_qsfpdd_info(port)    
    assert all (k in output for k in ("vendor","rx_pwr", "temp", "sn", "volt", "tx_bias"))

