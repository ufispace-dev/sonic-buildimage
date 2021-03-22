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
from bsp.const.const import CPLDSource, PortStatus, ResetStatus
from bsp.const.const import CPLDConst
from bsp.const.const import DevType
from bsp.cpld.cpld import CPLD

class CPLDUtility:

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.cpld = CPLD()

    def _check_cpld_num(self, cpld_num):
        if cpld_num not in range(CPLDConst.CPLD_MAX):                
            raise ValueError("CPLD number({0}) is out of range (0-{1})".format(cpld_num, CPLDConst.CPLD_MAX-1))

    def _check_dev_type(self, devType):
        if devType not in range(DevType.DEV_MAX):
            raise ValueError("Dev Type({}) is out of range (0-{})".format(devType, DevType.DEV_MAX))
        
        board_info = self.cpld.get_board_info()
        
        if board_info["hw_rev"] == 0:
            if devType != DevType.J2:
                raise ValueError("Dev Type({}) Reset is not supported ".format(devType))
        '''
        else:
            if devType not in range(DevType.RETIMER+1):
                raise ValueError("Dev Type({}) Reset is not supported ".format(devType))    
        '''
                
    def _version_h(self, version):
        return "{}.{:02d}".format(version >> 6,
                                  version & 0b00111111)

    def get_board_info(self):
        try:
            board_info = self.cpld.get_board_info()            
            return board_info
        except Exception as e:
            self.logger.error("get_board_info failed, error: {0}".format(e))

    def get_cpld_version(self, target):
        try:
            if target == CPLDSource.CPU:
                cpld_version = self.cpld.get_cpu_board_cpld_version()
                return {"version":"X.%02x" % cpld_version,
                        "version_h": self._version_h(cpld_version)}
            elif target == CPLDSource.MB:
                result = []
                result_h = []
                cpld_versions = self.cpld.get_main_board_cpld_version()
                for i in range(len(cpld_versions)):                    
                    result.append("X.%02x" % cpld_versions[i])
                    result_h.append(self._version_h(cpld_versions[i]))
                return {"version": result,
                        "version_h": result_h}
            else:
                raise ValueError("target(" + str(target) + ") is out of range")
            
        except Exception as e:
            self.logger.error("get_cpld_version failed, target={0}, error: {1}".format(target, e))
    
    def get_cpld_id(self):
        try:
            result = []
            cpld_ids = self.cpld.get_main_board_cpld_id()
            for i in range(len(cpld_ids)):                    
                result.append("X.%02x" % cpld_ids[i])
            return {"id": result}
        except Exception as e:
            self.logger.error("get_cpld_id failed, error: {0}".format(e))
                
    def get_cpld_port_interrupt(self, cpld_num):
        try:
            self._check_cpld_num(cpld_num)
            
            result = self.cpld.get_port_interrupt(cpld_num)            
            if result == PortStatus.INTERRUPTED:
                ret_val = {"interrupt_status":"interrupted"}
            else:
                ret_val = {"interrupt_status":"no interrupt"}
            return ret_val
        except Exception as e:
            self.logger.error("get_cpld_port_interrupt failed, error: {0}".format(e))

    def reset_dev(self, devType):
        try:
            self._check_dev_type(devType)
            self.cpld.reset_dev(devType)            
        except Exception as e:
            self.logger.error("reset_dev {} failed, error: {}".format(devType, e))
    
    def get_reset_ctrl(self, devType):
        try:            
            result = self.cpld.get_reset_ctrl(devType)
            
            if result == ResetStatus.RESET:
                ret_val = {"reset":"true"}
            elif result == ResetStatus.UNSET:
                ret_val = {"reset":"false"}
            else:
                ret_val = {"reset":"not supported"}
            return ret_val
        except Exception as e:
            self.logger.error("get_reset_ctrl {} failed, error: {}".format(devType, e))
                    
    def set_reset_ctrl(self, devType, reset_status):
        try:
            result = self.cpld.set_reset_ctrl(devType, reset_status)
            if result == False:
                self.logger.error("reset_ctrl failed, devType={}, reset_status={}".format(devType, reset_status))                            
        except Exception as e:
            self.logger.error("set_reset_ctrl {} failed, error: {}".format(devType, e))
            
