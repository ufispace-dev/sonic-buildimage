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

from bsp.utility.qsfp_utility import QSFPUtility
from bsp.const.const import QSFP, LPMode, PortStatus

@pytest.fixture(scope="session")
def util():
    return QSFPUtility()

ports = range(QSFP.MAX_PORT)

@pytest.mark.parametrize("port", ports)
def test_get_presence(util, port):
    expect = {"presence": "presence"}        
    
    output = util.get_presence(port)
    assert output == expect

@pytest.mark.parametrize("port", ports)
def test_get_lp_mode(util, port):
    expect = {"lp_mode":"disabled"}
    
    output = util.get_lp_mode(port)
    assert output == expect

@pytest.mark.parametrize("port", ports)
@pytest.mark.parametrize("lp_mode", [LPMode.DISABLE, LPMode.ENABLE, LPMode.DISABLE])
def test_set_lp_mode(util, port, lp_mode):
    expect = {"lp_mode":"enabled"} if lp_mode == LPMode.ENABLE else {"lp_mode":"disabled"}
        
    util.set_lp_mode(port, lp_mode)
    output = util.get_lp_mode(port)
    assert output == expect

@pytest.mark.parametrize("port", ports)
def test_get_reset(util, port):
    expect = {"reset":"false"}
    
    output = util.get_reset(port)
    assert output == expect

@pytest.mark.parametrize("port", ports)
@pytest.mark.parametrize("reset", [PortStatus.NO_RESET, PortStatus.RESET, PortStatus.NO_RESET])
def test_set_reset(util, port, reset):     
    expect = {"reset":"true"} if reset == PortStatus.RESET else {"reset":"false"}
    
    util.set_reset(port, reset)
    output = util.get_reset(port)
    assert output == expect

@pytest.mark.parametrize("port", ports)
def test_get_interrupt(util, port):
    expect = {"interrupt_status":"no interrupt"}
    
    output = util.get_interrupt(port)
    assert output == expect
        