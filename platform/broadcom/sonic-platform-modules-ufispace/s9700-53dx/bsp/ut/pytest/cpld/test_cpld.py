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

from bsp.utility.cpld_utility import CPLDUtility
from bsp.const.const import CPLDSource, CPLDConst, DevType, ResetStatus

devices = [DevType.J2, DevType.OP2_PERST]

@pytest.fixture(scope="session")
def util():
    return CPLDUtility()
    
def _compare_dict(output, expect):
    errors = []
    
    for key in output.keys():        
        if output[key] != expect[key]:
            errors.append("{} is {}, expect {}".format(key, output[key], expect[key]))
    
    return errors

def test_get_board_info(util):
    expect = {"hw_rev_str": "Beta",
            "build_rev_str": "A4",
            "hw_rev": 2,
            "board_id_str": "Apollo NCP1-1 40+13P",
            "board_id": 2,
            "build_rev": 3
            }        
    
    output = util.get_board_info()
    assert output == expect
     
def test_get_cpld_id(util):
    expect = {"id": [
        "X.00",
        "X.01",
        "X.02",
        "X.03",
        "X.04"
        ]}
        
    output = util.get_cpld_id()
    assert output == expect

@pytest.mark.parametrize("device", [CPLDSource.CPU, CPLDSource.MB])
def test_get_cpld_version(util, device):
    expect = [
        {
            "version": "X.1d",
            "version_h": "0.29"
        },
        {
            "version": [
                "X.4f",
                "X.14",
                "X.14",
                "X.14",
                "X.14"
            ],
            "version_h": [
                "1.15",
                "0.20",
                "0.20",
                "0.20",
                "0.20"
            ]
        }
    ]
        
    output = util.get_cpld_version(device)    
    assert output == expect[device]
    
@pytest.mark.parametrize("cpld_num", range(CPLDConst.CPLD_MAX))
def test_get_cpld_port_interrupt(util, cpld_num):
    #expect = {"interrupt_status":"interrupted"}
    expect = {"interrupt_status":"no interrupt"}
        
    output = util.get_cpld_port_interrupt(cpld_num)    
    assert output == expect

@pytest.mark.parametrize("device", devices)
def test_reset_ctrl(util, device):
    expect = [{"reset":"true"},
              {"reset":"false"} 
             ]
    
    #check device is not reset
    output = util.get_reset_ctrl(device)
    errors = _compare_dict(output, expect[ResetStatus.UNSET])
    if len(errors) != 0:
        assert not errors, "errors occured:\n{}".format("\n".join(errors))
    
    #reset device    
    util.set_reset_ctrl(device, ResetStatus.RESET)    
    
    #check device is reset
    output = util.get_reset_ctrl(device)
    errors = _compare_dict(output, expect[ResetStatus.RESET])
    if len(errors) != 0:
        assert not errors, "errors occured:\n{}".format("\n".join(errors))
    
    #unset device
    util.set_reset_ctrl(device, ResetStatus.UNSET)
    
    #check device is unset
    output = util.get_reset_ctrl(device)
    errors = _compare_dict(output, expect[ResetStatus.UNSET])
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

