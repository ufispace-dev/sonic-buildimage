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
from bsp.const.const import PortStatus
from bsp.const.const import LPMode
from bsp.const.const import QSFPDD
from bsp.cpld.cpld import CPLD

class QSFPDDUtility:
            
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()        
        self.cpld = CPLD()

    def _check_qsfpdd_port(self, port):
        if port not in range(QSFPDD.MAX_PORT):                
            raise ValueError("Port number({0}) is out of range (0-{1})".format(port, QSFPDD.MAX_PORT-1))
    
    def _check_enable(self, enable):
        if enable not in range(LPMode.ENABLE+1):
            raise ValueError("enable ({0}) is out of range (0-{1})".format(enable, LPMode.ENABLE))    
    
    def _check_reset(self, reset):
        if reset not in range(PortStatus.NO_RESET+1):
            raise ValueError("reset ({0}) is out of range (0-{1})".format(reset, PortStatus.NO_RESET))
        
    def get_presence(self, port_num):
        try:
            self._check_qsfpdd_port(port_num)

            result = self.cpld.qsfpdd_get_presence(port_num)

            if result == PortStatus.PORT_ABSENCE:
                ret_val = {"presence":"absence"}
            else:
                ret_val = {"presence":"presence"}

            return ret_val
        except Exception as e:
            self.logger.error("get_presence failed, port_num={0}, error: {1}".format(port_num, e))

    def get_interrupt(self, port_num):
        try:
            self._check_qsfpdd_port(port_num)

            result = self.cpld.qsfpdd_get_interrupt(port_num)

            if result == PortStatus.INTERRUPTED:
                ret_val = {"interrupt_status":"interrupted"}
            else:
                ret_val = {"interrupt_status":"no interrupt"}

            return ret_val
        except Exception as e:
            self.logger.error("get_port_interrupt failed, error: {0}".format(e))
            
    def set_lp_mode(self, port_num, enable):
        try:
            self._check_qsfpdd_port(port_num)
            self._check_enable(enable)            
            
            self.cpld.qsfpdd_set_lp_mode(port_num, enable)
        except Exception as e:
            self.logger.error("set_lp_mode failed, port_num={0}, enable={1}, error: {2}".format(port_num, enable, e))

    def get_lp_mode(self, port_num):
        try:
            self._check_qsfpdd_port(port_num)

            result = self.cpld.qsfpdd_get_lp_mode(port_num)

            if result == LPMode.DISABLE:
                ret_val = {"lp_mode":"disabled"}
            else:
                ret_val = {"lp_mode":"enabled"}

            return ret_val
        except Exception as e:
            self.logger.error("get_lp_mode failed, port_num={0}, error: {1}".format(port_num, e))

    def reset_port(self, port_num):
        try:
            self._check_qsfpdd_port(port_num)

            self.cpld.qsfpdd_reset_port(port_num)
        except Exception as e:
            self.logger.error("reset_port failed, port_num={0}, error: {1}".format(port_num, e))
    
    def get_reset(self, port_num):
        try:
            self._check_qsfpdd_port(port_num)

            result = self.cpld.qsfpdd_get_reset(port_num)
            if result == PortStatus.RESET:
                ret_val = {"reset":"true"}
            else:
                ret_val = {"reset":"false"}

            return ret_val
        except Exception as e:
            self.logger.error("get_reset failed, port_num={0}, error: {1}".format(port_num, e))
    
    def set_reset(self, port_num, reset):
        try:
            self._check_qsfpdd_port(port_num)
            self._check_reset(reset)

            self.cpld.qsfpdd_set_reset(port_num, reset)            
        except Exception as e:
            self.logger.error("set_reset failed, port_num={0}, error: {1}".format(port_num, e))
