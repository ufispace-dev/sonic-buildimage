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

from bsp.utility.psu_utility import PSUUtility
from bsp.const.const import PSU

psus = range(PSU.MAX_PSU)

@pytest.fixture(scope="session")
def util():
    return PSUUtility()

@pytest.mark.parametrize("psu", psus)
def test_get_psu_presence(util, psu):
    expect = {'presence': 'presence'}        
    
    output = util.get_psu_presence(psu)
    assert output == expect

@pytest.mark.parametrize("psu", psus)
def test_get_psu_power_ok(util, psu):
    expect = {"power":"ok"}        
    
    output = util.get_psu_power_ok(psu)
    assert output == expect
    