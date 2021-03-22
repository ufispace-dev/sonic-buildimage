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
from bsp.thermal.thermal import Thermal

class ThermalUtility:

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.thermal = Thermal()

    def get_cpu_board_tmp75(self):
        try:
            content = self.thermal.get_tmp75_cpu_board()

            return {"cpu_board_tmp75_temp":content}
        except Exception as e:
            self.logger.error("get_cpu_board_tmp75 failed, error: {}".format(str(e)))

    def get_cpu_core_temp(self):
        core_num = 8
        ret_val = {}
        
        try:
            ret_val["package_temp"] = self.thermal.get_coretemp_cpu(1)
            for i in range(core_num):
                key = "core{}_temp".format(i+1)
                ret_val[key] = self.thermal.get_coretemp_cpu(i+2)
            
            return ret_val

        except Exception as e:
            self.logger.error("get_cpu_core_temp failed, error: {0}".format(str(e)))
