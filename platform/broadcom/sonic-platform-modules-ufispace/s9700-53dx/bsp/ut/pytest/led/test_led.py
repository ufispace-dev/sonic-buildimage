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
from utility.led_utility import LEDUtility
from const.const import Led, QSFPDD

beacon_nums = [
    0x00, 
    0x11, 0x22, 0x33, 0x44, 0x55, 
    0x66, 0x77, 0x88, 0x99, 0xaa, 
    0xbb, 0xcc, 0xdd, 0xee, 0xff]
ports = range(QSFPDD.MAX_PORT)         
colors = range(Led.COLOR_MAX)
blinks = range(Led.BLINK_STATUS_MAX)

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
def util():
    return LEDUtility()

@pytest.mark.parametrize("target", 
                         [Led.SYSTEM, Led.FAN, Led.PSU0, Led.PSU1],
                         )
def test_get_sys_led(util, target):
    expect = {
        "color": "GREEN",
        "blink": "Solid",
        "onoff": "ON"
    }
      
    output = util.get_sys_led(target)
    assert output == expect

@pytest.mark.skip(reason="covered in test_set_qsfpdd_led")
@pytest.mark.parametrize("port", ports)
def test_get_qsfpdd_led(util, port):
    expect = {
        "color": "OFF",
        "blink": "solid"
    }        
    
    output = util.get_qsfpdd_led(port)
    assert output == expect
    
@pytest.mark.parametrize("port", ports)
@pytest.mark.parametrize("color", colors, ids=["OFF", "RED", "GREEN", "BLUE"])
@pytest.mark.parametrize("blink", blinks, ids=["SOLID", "BLINK"])
def test_set_qsfpdd_led(util, port, color, blink):
    expect = {
        "color": "",
        "blink": ""
    }        
    
    if color == Led.COLOR_GREEN:
        expect["color"] = "GREEN"
    elif color == Led.COLOR_RED:
        expect["color"] = "RED"
    elif color == Led.COLOR_BLUE:
        expect["color"] = "BLUE"
    else:
        expect["color"] = "OFF"
    
    if blink == Led.BLINK_STATUS_BLINKING:
        expect["blink"] = "blinking"
    else:
        expect["blink"] = "solid"
    
    if color == Led.COLOR_OFF and blink == Led.BLINK_STATUS_BLINKING:
        pytest.xfail("blinking off is not valid combination")
        
    util.set_qsfpdd_led(port, color, blink)    
    output = util.get_qsfpdd_led(port)
    assert output == expect

@pytest.mark.parametrize("beacon_num", beacon_nums)
def test_set_beacon_led_num(util, beacon_num): 
    
    util.set_beacon_led_num(beacon_num)
    #time.sleep(0.5)
    assert True                                                     
    
@pytest.mark.skip(reason="manually test")
@pytest.mark.parametrize("beacon_num", beacon_nums)   
def test_set_beacon_led_num_input(util, suspend_capture, beacon_num): 
    
    with suspend_capture:
        util.set_beacon_led_num(beacon_num)
        input("press any key to continue: ")        
        