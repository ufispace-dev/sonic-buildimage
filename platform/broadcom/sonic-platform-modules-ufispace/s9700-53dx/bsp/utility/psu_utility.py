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
from bsp.cpld.cpld import CPLD
from bsp.const.const import PSUStatus
from bsp.const.const import PSU

class PSUUtility:
        
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.cpld = CPLD()        
    
    def _check_psu_range(self, psu_num):
        if psu_num not in range(PSU.MAX_PSU):                
            raise ValueError("PSU number({0}) is out of range (0-{1})".format(psu_num, PSU.MAX_PSU-1))
                
    def get_psu_presence(self, psu_num):
        try:
            self._check_psu_range(psu_num)
            
            result = self.cpld.get_psu_presence(psu_num)
            if result == PSUStatus.ABSENCE:
                ret_val = {"presence":"absence"}
            else:
                ret_val = {"presence":"presence"}

            return ret_val
        except Exception as e:
            self.logger.error("get_psu_presence failed, psu_num={}, error: {}".format(psu_num, e))                    
        
    def get_psu_power_ok(self, psu_num):
        try:
            self._check_psu_range(psu_num)
            
            result = self.cpld.get_psu_power_ok(psu_num)
            if result == PSUStatus.POWER_FAIL:
                ret_val = {"power":"failed"}
            else:
                ret_val = {"power":"ok"}

            return ret_val
        except Exception as e:
            self.logger.error("get_psu_power_ok failed, psu_num={0}, error: {1}".format(psu_num, e))
