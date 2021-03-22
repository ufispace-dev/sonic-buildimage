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
from bsp.ipmi.ipmitool import IPMITool 

class IPMIUtility:

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.ipmitool = IPMITool()
    
    def get_sensor(self, keyword=""):        
        try:
            sensors = self.ipmitool.get_sensor(keyword)
            return sensors
        except Exception as e:
            self.logger.error("get_sensor failed, error: {0}".format(e))
    
    def get_ipmidev_status(self):
        try:
            is_exist = self.ipmitool.is_ipmidev_exist()
            return {"is_ipmidev_exist": is_exist}
        except Exception as e:
            self.logger.error("is_ipmidev_exist() failed, error: {0}".format(e))
