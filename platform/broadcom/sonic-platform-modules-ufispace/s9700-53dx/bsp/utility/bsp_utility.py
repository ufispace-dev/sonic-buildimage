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
from bsp.utility.sysfs_utility import SysfsUtility
import os

class BSPUtility:

    version = "4.1.0"
    
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.sysfs_util = SysfsUtility()
        
    def get_version(self):
        try:
            return {"version": self.version}                
        except Exception as e:
            self.logger.error("get_version failed, error: {}".format(e))

    def is_bsp_inited(self):
        try:            
            bus_path_1 = self.sysfs_util.get_bus_path(1)
            gpio511_path = self.sysfs_util.get_gpio_path(511)
            gpio255_path = self.sysfs_util.get_gpio_path(255)
            
            if (os.path.exists(bus_path_1)):
                self.logger.info("[is_bsp_inited] sysfs {} exists".format(bus_path_1))
                return True
            elif os.path.exists(gpio511_path) or os.path.exists(gpio255_path):
                return True
            else:
                return False                
        except Exception as e:
            self.logger.error("is_bsp_inited failed, error: {}".format(e))
            