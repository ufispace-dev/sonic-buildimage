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
import subprocess
from eeprom.eeprom import EEPRom
from const.const import QSFP, QSFPDD
from utility.qsfp_utility import QSFPUtility
from utility.qsfpdd_utility import QSFPDDUtility

qsfp_ports = range(QSFP.MAX_PORT)
qsfpdd_ports = range(QSFPDD.MAX_PORT)

@pytest.fixture
def suspend_capture(pytestconfig):
    class suspend_guard:
        def __init__(self):
            self.capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')
        def __enter__(self):
            self.capmanager.suspend_global_capture(in_=True)
        def __exit__(self, _1, _2, _3):
            self.capmanager.resume_global_capture()

    yield suspend_guard()
    
@pytest.fixture(scope="session")
def eeprom():
    return EEPRom()

@pytest.fixture(scope="session")
def qsfp_util():
    return QSFPUtility()

@pytest.fixture(scope="session")
def qsfpdd_util():
    return QSFPDDUtility()

@pytest.mark.parametrize("port", qsfp_ports)
def test_qsfp_eeprom(suspend_capture, eeprom, qsfp_util, port):    
    cmd = "dd if={}/eeprom bs=128 count=1 skip=1 status=none | hd"
    
    if (qsfp_util.get_presence(port)["presence"] != "presence"):
        pytest.skip("Module not present")
        
    sysfs = eeprom.get_eeprom_sysfs(eeprom.DEV_TYPE_QSFP, port)
    retcode, output0 = subprocess.getstatusoutput(cmd.format(sysfs))
    
    #with suspend_capture:
    #    print(output0)
    
    for i in range(100):    
        retcode, output1 = subprocess.getstatusoutput(cmd.format(sysfs))
        assert output0 == output1

@pytest.mark.parametrize("port", qsfpdd_ports)
def test_qsfpdd_eeprom(suspend_capture, eeprom, qsfpdd_util, port):    
    cmd = "dd if={}/eeprom bs=128 count=1 skip=1 status=none | hd"
    
    if (qsfpdd_util.get_presence(port)["presence"] != "presence"):
        pytest.skip("Module not present")
        
    sysfs = eeprom.get_eeprom_sysfs(eeprom.DEV_TYPE_QSFPDD, port)
    retcode, output0 = subprocess.getstatusoutput(cmd.format(sysfs))
    
    #with suspend_capture:
    #    print(output0)
    
    for i in range(100):    
        retcode, output1 = subprocess.getstatusoutput(cmd.format(sysfs))
        assert output0 == output1
        