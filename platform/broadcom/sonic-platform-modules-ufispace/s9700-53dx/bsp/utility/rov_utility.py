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
from bsp.rov.rov import ROVController

class ROVUtility:
           
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.cpld = CPLD()
        self.rov_controller = ROVController()
   
    def platform_check(self):
        # NCP 1-1 beta (JR2 B1) and later
        #0x2[9abcdefABCDEF])        
        board_info = self.cpld.get_board_info()        
        if board_info["hw_rev"] >= 2:
            return True
        else:
            return False
           
    def get_j2_rov(self):
        try:
            if not self.platform_check():
                self.logger.error("Not supported")                
                return {}
            
            j2_rov_stamp = self.cpld.get_j2_rov_stamp()
            rov_controller_config = self.rov_controller.get_rov_config()
            rov_controller_output = self.rov_controller.get_rov_output()
            return {"j2_rov_stamp": j2_rov_stamp,
                    "rov_controller_config": "0x{:02X}".format(rov_controller_config),
                    "rov_controller_config_volt": self.rov_controller._vid_to_volt_str(rov_controller_config),
                    "rov_controller_output": "0x{:02X}".format(rov_controller_output),
                    "rov_controller_output_volt": self.rov_controller._vid_to_volt_str(rov_controller_output)
                    }
        except Exception as e:
            self.logger.error("get_j2_rov failed, error: {0}".format(e))
    
    def set_j2_rov(self):
        try:
            if not self.platform_check():
                self.logger.error("Not supported")   
                return
            
            j2_rov_stamp = self.cpld.get_j2_rov_stamp()
            self.rov_controller.set_rov_config(j2_rov_stamp)
            
        except Exception as e:
            self.logger.error("set_j2_rov failed, error: {}".format(e))
            