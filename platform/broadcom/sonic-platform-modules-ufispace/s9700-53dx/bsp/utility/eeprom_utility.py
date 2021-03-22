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
from bsp.eeprom.eeprom import EEPRom
from bsp.const.const import QSFP
from bsp.const.const import QSFPDD
from bsp.const.const import PortStatus
from bsp.cpld.cpld import CPLD

class EEPRomUtility:
    
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.eeprom = EEPRom()
        self.cpld = CPLD()

    def _check_qsfp_port(self, port_num):
        if port_num not in range(QSFP.MAX_PORT):
            raise ValueError("Port number(" + str(port_num) + ") is out of range")            
        elif self.cpld.qsfp_get_presence(port_num) == PortStatus.PORT_ABSENCE:            
            raise ValueError("QSFP(" + str(port_num) + ") is not present")
    
    def _check_qsfpdd_port(self, port_num):
        if port_num not in range(QSFPDD.MAX_PORT):
            raise ValueError("Port number(" + str(port_num) + ") is out of range")      
        elif self.cpld.qsfpdd_get_presence(port_num) == PortStatus.PORT_ABSENCE:            
            raise ValueError("QSFPDD(" + str(port_num) + ") is not present")
                
    def dump_cpu_eeprom(self):
        try:
            content = self.eeprom.dump_cpu_eeprom()

            return {"content":content}
        except Exception:
            raise

    '''
    def dump_sfp_eeprom(self, port_num):
        try:
            if port_num not in range(SFP.MAX_PORT):
                raise ValueError("Port number(" + str(port_num) + ") is out of range")

            content = self.eeprom.dump_sfp_eeprom(port_num)

            return {"content":content}
        except Exception as e:
            raise
    '''

    def dump_qsfp_eeprom(self, port_num):
        try:
            self._check_qsfp_port(port_num)

            content = self.eeprom.dump_qsfp_eeprom(port_num)

            return {"content":content}
        except Exception:
            raise
    
    def dump_qsfpdd_eeprom(self, port_num):
        try:
            self._check_qsfpdd_port(port_num)

            content = self.eeprom.dump_qsfpdd_eeprom(port_num)

            return {"content":content}
        except Exception:
            raise
    
    def get_qsfp_info(self, port_num):
        try:
            self._check_qsfp_port(port_num)

            content = self.eeprom.get_qsfp_info(port_num)

            return content
        except Exception:
            raise    
        
    def get_qsfpdd_info(self, port_num):
        try:
            self._check_qsfpdd_port(port_num)

            content = self.eeprom.get_qsfpdd_info(port_num)

            return content
        except Exception:
            raise    

    def get_qsfp_bus_num(self, port_num):
        try:
            bus_num = self.eeprom._get_qsfp_bus_num(port_num)
            return bus_num
        except Exception:
            raise

    def get_qsfpdd_bus_num(self, port_num):
        try:
            bus_num = self.eeprom._get_qsfpdd_bus_num(port_num)
            return bus_num
        except Exception:
            raise

    def dump_sysfs(self):
        try:
            content = self.eeprom.dump_sysfs()

            return content
        except Exception:
            raise

