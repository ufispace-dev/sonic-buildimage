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
from bsp.utility.thermal_utility import ThermalUtility

@pytest.fixture(scope="session")
def util():
    return ThermalUtility()

@pytest.fixture(scope="session")
def threshold():
    return {"low": 0,
            "high": 100000}

def test_get_cpu_board_tmp75(util, threshold):    
    output = util.get_cpu_board_tmp75()
    assert threshold["low"] <= output["cpu_board_tmp75_temp"] <= threshold["high"]
    
def test_get_cpu_core_temp(util, threshold):    
    output = util.get_cpu_core_temp()
    for key in output.keys():
        assert threshold["low"] <= output[key] <= threshold["high"]
