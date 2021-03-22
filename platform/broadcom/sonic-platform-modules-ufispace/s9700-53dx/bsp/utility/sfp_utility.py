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
from bsp.const.const import SFP
from bsp.const.const import PortStatus
from bsp.gpio.ioexp import IOExpander
from bsp.cpld.cpld import CPLD

class SFPUtility:
    
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.ioexp = IOExpander()
        self.cpld = CPLD()

    def _check_sfp_port(self, port):
        if port not in range(SFP.MAX_PORT):                
            raise ValueError("Port number({0}) is out of range (0-{1})".format(port, SFP.MAX_PORT-1))
        
    def get_presence(self, port_num):
        try:
            #get hw_rev
            board_info = self.cpld.get_board_info()
            
            #not proto board
            if board_info["hw_rev"] != 0b00 :
                ret_val = {"presence":"not supported"}
                return ret_val
            
            self._check_sfp_port(port_num)

            result = self.cpld.sfp_get_presence(port_num)

            if result == PortStatus.PORT_ABSENCE:
                ret_val = {"presence":"absence"}
            else:
                ret_val = {"presence":"presence"}

            return ret_val
        except Exception as e:
            self.logger.error("get_presence failed, port_num={0}, error: {1}".format(port_num, e))

    def get_rx_los(self, port_num):
        try:
            self._check_sfp_port(port_num)

            result = self.cpld.sfp_get_rx_los(port_num)

            if result == SFP.DETECTED:
                ret_val = {"rx_los":"detected"}
            else:
                ret_val = {"rx_los":"undetected"}

            return ret_val
        except Exception as e:
            self.logger.error("get_rx_los failed, port_num={0}, error: {1}".format(port_num, e))

    def get_tx_fault(self, port_num):
        try:
            self._check_sfp_port(port_num)

            result = self.cpld.sfp_get_tx_fault(port_num)

            if result == SFP.DETECTED:
                ret_val = {"tx_flt":"detected"}
            else:
                ret_val = {"tx_flt":"undetected"}

            return ret_val
        except Exception as e:
            self.logger.error("get_tx_fault failed, port_num={0}, error: {1}".format(port_num, e))

    def set_tx_disable(self, port_num, tx_disable):
        try:
            self._check_sfp_port(port_num)

            if tx_disable not in range(SFP.DISABLED+1):
                raise ValueError("tx_disable ({0}) is out of range (0-{1})".format(tx_disable, SFP.DISABLED))
            
            self.cpld.sfp_set_tx_disable(port_num, tx_disable)
        except Exception as e:
            self.logger.error("set_tx_disable failed, port_num={0}, tx_disable={1}, error: {2}".format(port_num, tx_disable, e))

    def get_tx_disable(self, port_num):
        try:
            self._check_sfp_port(port_num)

            result = self.cpld.sfp_get_tx_disable(port_num)

            if result == PortStatus.ENABLED:
                ret_val = {"tx_disable":"enabled"}
            else:
                ret_val = {"tx_disable":"disabled"}

            return ret_val
        except Exception as e:
            self.logger.error("get_tx_disable failed, port_num={0}, error: {1}".format(port_num, e))

