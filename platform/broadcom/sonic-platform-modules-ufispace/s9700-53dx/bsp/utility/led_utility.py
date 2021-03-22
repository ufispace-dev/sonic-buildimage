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

import time

from bsp.common.logger import Logger
from bsp.led.led import SYS_LED
from bsp.led.beacon_led import BEACON_LED
from bsp.cpld.cpld import CPLD
from bsp.const.const import Led
from bsp.const.const import QSFPDD

class LEDUtility:

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.sys_led = SYS_LED()
        self.cpld = CPLD()
        self.beacon_led = BEACON_LED()
    
    def _check_led_color(self, color):
        if color not in range(Led.COLOR_MAX):                
            raise ValueError("Color ({0}) is out of range (0-{1})".format(color, Led.COLOR_MAX-1))
    
    def _check_sys_led(self, target):                
        if target not in range(Led.PSU1+1):                
            raise ValueError("LED type({0}) is out of range (0-{1})".format(target, Led.PSU1))
            
    def _check_qsfpdd_port(self, port):
        if port not in range(QSFPDD.MAX_PORT):                
            raise ValueError("Port number({0}) is out of range (0-{1})".format(port, QSFPDD.MAX_PORT-1))
    
    def _check_qsfpdd_led_blink(self, blink):
        if blink not in range(Led.BLINK_STATUS_MAX):                
            raise ValueError("Blink Status({0}) is out of range (0-{1})".format(blink, Led.BLINK_STATUS_MAX-1))
    
    def _check_beacon_num(self, beacon_num):                
        if beacon_num not in range(Led.BEACON_MAX+1):                
            raise ValueError("Beacon number({0}) is out of range (0-{1})".format(beacon_num, Led.BEACON_MAX))
                    
    def get_sys_led(self, target):
        result = {"color": "", "blink": "", "onoff": ""}
        try:
            
            color, blink, onoff = self.sys_led.get_sys_led(target)
            
            if color == 1:
                result["color"] = "GREEN"
            else:
                result["color"] = "YELLOW"
                
            if blink == 1:
                result["blink"] = "Blinking"
            else:
                result["blink"] = "Solid"
            
            if onoff == 1:
                result["onoff"] = "ON"
            else:
                #clear other fileds if led is off
                result["color"] = ""
                result["blink"] = ""
                result["onoff"] = "OFF"
                    
            return result
            
        except Exception as e:
            self.logger.error("get_sys_led failed, error: {}".format(e))
                    
    def set_sys_led(self, target, color, blink=-1):
        try:
            self._check_sys_led(target)
            self._check_led_color(color)
            if blink != -1:
                self._check_qsfpdd_led_blink(blink)
                        
            self.sys_led.set_led(target, color, blink)
        except Exception as e:
            self.logger.error("set_sys_led failed, led={}, color={}, error: {}".format(target, color, e))
            
    def set_qsfpdd_led(self, port, color, blink):
        try:
            self._check_qsfpdd_port(port)
            self._check_led_color(color)
            self._check_qsfpdd_led_blink(blink)
            
            self.cpld.set_qsfpdd_led(port, color, blink)
        except Exception as e:
            self.logger.error("set_qsfpdd_led failed, port={}, color={}, blink={}, error: {}".format(port, color, blink, e))
            
    def get_qsfpdd_led(self, port):
        result = {"color": "", "blink": ""}
        try:
            self._check_qsfpdd_port(port)
            
            led_status = self.cpld.get_qsfpdd_led(port)
            color = led_status[0]
            blink = led_status[1]
            
            if color == Led.COLOR_GREEN:
                result["color"] = "GREEN"
            elif color == Led.COLOR_RED:
                result["color"] = "RED"
            elif color == Led.COLOR_BLUE:
                result["color"] = "BLUE"
            else:
                result["color"] = "OFF"
            
            if blink == Led.BLINK_STATUS_BLINKING:
                result["blink"] = "blinking"
            else:
                result["blink"] = "solid"
                
            return result
            
        except Exception as e:
            self.logger.error("set_qsfpdd_led failed, port={}, color={}, error: {}".format(port, color, e))
            
    def set_beacon_led_num(self, beacon_num):
        try:
            self._check_beacon_num(beacon_num)            
                        
            self.beacon_led.set_beacon_num(beacon_num)            
        except Exception as e:
            self.logger.error("set_beacon_num failed, num={}, error: {}".format(beacon_num, e))

    def ut_sysled(self):
        color_desc = ["Green", "Yellow", "Off"]         
        for i, color in enumerate([Led.COLOR_GREEN, Led.COLOR_YELLOW, Led.COLOR_OFF]):
            self.logger.error("[Sys LED] -- {0}".format(color_desc[i]))
            for led in [Led.SYSTEM, Led.FAN, Led.PSU0, Led.PSU1]:                            
                self.set_sys_led(led, color)
                time.sleep(0.5)
  
        self.logger.info("[Sys LED] -- End")
        
    def ut_qsfpdd_led(self):
        blink_desc = ["Solid", "Blinking"]
        color_desc = ["Green", "Red", "Blue", "Off"]
                
        for i, blink in enumerate([Led.BLINK_STATUS_SOLID, Led.BLINK_STATUS_BLINKING]):
            for j, color in enumerate([Led.COLOR_GREEN, Led.COLOR_RED, Led.COLOR_BLUE, Led.COLOR_OFF]):
                if blink == Led.BLINK_STATUS_BLINKING and color == Led.COLOR_OFF :
                        continue
                self.logger.error("[QSFPDD LED] -- {0} {1}".format(blink_desc[i], color_desc[j]))
                for port in range(QSFPDD.MAX_PORT):   
                            
                    self.set_qsfpdd_led(port, color, blink)
                    time.sleep(1)
        
        time.sleep(1)
        self.logger.error("[QSFPDD LED] -- End")
        for port in range(QSFPDD.MAX_PORT):            
            self.set_qsfpdd_led(port, Led.COLOR_OFF, Led.BLINK_STATUS_SOLID)

    def ut_beacon_led(self):                 
        for _, beacon_num in enumerate([0x00, 
                                    0x11, 0x22, 0x33, 0x44, 0x55, 
                                    0x66, 0x77, 0x88, 0x99, 0xaa, 
                                    0xbb, 0xcc, 0xdd, 0xee, 0xff]):
            self.logger.error("[Beacon LED] -- {:02x}".format(beacon_num))
            self.set_beacon_led_num(beacon_num)
            time.sleep(0.5)
  
        self.logger.info("[Beacon LED] -- End")
