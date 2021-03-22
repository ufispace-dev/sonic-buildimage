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

from bsp.common.logger import Logger
from bsp.const.const import Led
from bsp.const.const import BID
from bsp.cpld.cpld import CPLD
from bsp.utility.board_id_utility import BrdIDUtility

class SYS_LED:        
        
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.brd_id_util = BrdIDUtility()
        self.board_id = self.brd_id_util.get_board_id()
         
        self.cpld = CPLD()       
                 
    def get_sys_led(self, target):
        try:
            reg_val = self.cpld.get_sys_led(target)
            
            # get color
            color = reg_val & Led.MASK_COLOR
            blink = (reg_val & Led.MASK_BLINK) >> 2
            onoff = (reg_val & Led.MASK_ONOFF) >> 3
                        
            return (color, blink, onoff)
                
        except Exception as e:  
            self.logger.error(e)          
            raise       

    def set_led(self, target, color, blink):
        # disable set_led function due to this design will be changed in the future.
        return
        try:
            #proto or alpha
            if (self.board_id & BID.BUILD_REV_MASK) < BID.NCP1_1_BETA:
                if target == Led.SYSTEM:                
                    if color == Led.COLOR_GREEN:
                        self.ioexp.set_sys_led_g(1)
                    elif color == Led.COLOR_RED:
                        self.ioexp.set_sys_led_g(0)
                    else:                    
                        raise ValueError("Led.SYSTEM does not support COLOR_OFF")
                elif target == Led.FAN:                
                    if color == Led.COLOR_GREEN:
                        self.ioexp.set_fan_led_en(1)
                        self.ioexp.set_fan_led_y(0)
                    elif color == Led.COLOR_RED:
                        self.ioexp.set_fan_led_en(1)
                        self.ioexp.set_fan_led_y(1)
                    else:
                        self.ioexp.set_fan_led_en(0)                    
                elif target == Led.PSU0:                
                    if color == Led.COLOR_GREEN:
                        self.ioexp.set_psu0_led_y(0)
                        self.ioexp.set_psu0_pwrok(1)                                        
                    elif color == Led.COLOR_RED:
                        self.ioexp.set_psu0_led_y(1)
                        self.ioexp.set_psu0_pwrok(1)
                    else:                    
                        self.ioexp.set_psu0_pwrok(0)                                        
                elif target == Led.PSU1:
                    if color == Led.COLOR_GREEN:
                        self.ioexp.set_psu1_led_y(0)
                        self.ioexp.set_psu1_pwrok(1)                                        
                    elif color == Led.COLOR_RED:
                        self.ioexp.set_psu1_led_y(1)
                        self.ioexp.set_psu1_pwrok(1)
                    else:                    
                        self.ioexp.set_psu1_pwrok(0)    
                else:
                    raise ValueError("This LED type is not supported")
            #beta or later
            else:
                self.cpld.set_sys_led(target, color, blink)
                print("Sys LEDs are controlled by BMC since BETA board")
        except Exception as e:  
            self.logger.error(e)          
            raise       
    
    def init(self):
        pass

    def deinit(self):
        pass
