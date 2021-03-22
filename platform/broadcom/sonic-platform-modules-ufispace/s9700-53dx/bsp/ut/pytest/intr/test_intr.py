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
from bsp.utility.intr_utility import INTRUtility

@pytest.fixture(scope="session")
def util():
    return INTRUtility()

def test_init_i2c_alert(util):
    
    util.init_i2c_alert()
    assert util.get_alert_gpio() == 0
    assert util.get_alert_dis() == 0

def test_clear_i2c_alert(util):
    
    util.clear_i2c_alert()
    assert util.get_alert_sts() == 0    
        
def test_get_cpld_to_cpu_intr(util):
    expect = {
        "op2": 1,
        "cpld_1_2": 1,
        "cpld_3": 1,
        "cpld_4": 1,
        "cpld_5": 1,
        "j2": 1
    }
    
    output = util.get_cpld_to_cpu_intr()
    assert output == expect

def test_get_all_cpld_intr(util):
    expect = {
        "cpld_1": {
            "port_intr": 1,
            "gearbox": 1,
            "usb": 1,
            "port_presence": 1,
            "psu0": 1,
            "psu1": 1,
            "pex8724": 1,
            "cs4227": 1,
            "retimer": 1
        },
        "cpld_2": {
            "port_intr": 1,
            "port_presence": 1
        },
        "cpld_3": {
            "port_intr": 1,
            "port_presence": 1
        },
        "cpld_4": {
            "port_intr": 1,
            "port_presence": 1
        },
        "cpld_5": {
            "port_intr": 1,
            "port_presence": 1
        }
    }
    
    output = util.get_all_cpld_intr()
    assert output == expect

def test_get_gbox_intr(util):
    expect = {
        "gearbox_0": 1,
        "gearbox_1": 1,
        "gearbox_2": 1,
        "gearbox_3": 1,
        "gearbox_4": 1,
        "gearbox_5": 1,
        "gearbox_6": 1,
        "gearbox_7": 1,
        "gearbox_8": 1,
        "gearbox_9": 1
    }
    
    output = util.get_gbox_intr()
    assert output == expect
    
def test_get_retimer_intr(util):
    expect = {
        "retimer_0": 1,
        "retimer_1": 1,
        "retimer_2": 1,
        "retimer_3": 1,
        "retimer_4": 1
    }
    
    output = util.get_retimer_intr()
    assert output == expect
    
def test_deinit_i2c_alert(util):
    
    util.deinit_i2c_alert()
    assert util.get_alert_dis() == 1
        