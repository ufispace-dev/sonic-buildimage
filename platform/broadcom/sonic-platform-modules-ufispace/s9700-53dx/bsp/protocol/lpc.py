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

import portio
from enum import Enum

from bsp.common.logger import Logger

class LPCDevType(Enum):
    CPLD_ON_CPU_BOARD = 0
    CPLD_ON_MAIN_BOARD = 1
    BDE_GPIO_ON_CPU_BOARD = 2
    CPU_I2C_ALERT = 3

class LPC:

    BASE_ADDR = {LPCDevType.CPLD_ON_CPU_BOARD: 0x600,
                 LPCDevType.CPLD_ON_MAIN_BOARD: 0x700,
                 LPCDevType.BDE_GPIO_ON_CPU_BOARD: 0x500,
                 LPCDevType.CPU_I2C_ALERT: 0xf000}

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.lpcAddr = self.BASE_ADDR[LPCDevType.CPLD_ON_CPU_BOARD]

    def _devAddrSet(self, dev_type):        
        if dev_type in self.BASE_ADDR.keys():
            self.lpcAddr = self.BASE_ADDR[dev_type]                    
        else:
            raise ValueError("Invalid device dev_type: " + str(dev_type))

    def regGet(self, dev_type, addr):
        try:
            self._devAddrSet(dev_type)
        except Exception as e:
            self.logger.error("Set device address fail, error: " + str(e))
            raise

        try:
            portio.iopl(3)
        except Exception as e:
            self.logger.error("LPC.regGet: iopl() enable failed")
            raise

        try:
            portio.ioperm(self.lpcAddr + addr, 4, 1)
        except Exception as e:
            self.logger.error("LPC.regGet: ioperm() enable failed")
            raise

        try:
            getValue = portio.inb(self.lpcAddr + addr)
        except Exception as e:
            self.logger.error("LPC.regGet: inb() failed")

        try:
            portio.ioperm(self.lpcAddr + addr, 4, 0)
        except Exception as e:
            self.logger.error("LPC.regGet: ioperm() disable failed")
            raise

        try:
            portio.iopl(0)
        except Exception as e:
            self.logger.error("LPC.regGet: iopl() disable failed")
            raise

        return getValue

    def regSet(self, dev_type, addr, data):
        try:
            self._devAddrSet(dev_type)
        except Exception as e:
            self.logger.error("Set device address fail, error: " + str(e))
            raise

        try:
            portio.iopl(3)
        except Exception as e:
            self.logger.error("LPC.regGet: iopl() enable failed")
            raise

        try:
            portio.ioperm(self.lpcAddr + addr, 4, 1)
        except Exception as e:
            self.logger.error("LPC.regGet: ioperm() enable failed")
            raise

        try:
            portio.outb(data, self.lpcAddr + addr)
        except Exception as e:
            self.logger.error("LPC.regGet: outb() failed")

        try:
            portio.ioperm(self.lpcAddr + addr, 4, 0)
        except Exception as e:
            self.logger.error("LPC.regGet: ioperm() disable failed")
            raise

        try:
            portio.iopl(0)
        except Exception as e:
            self.logger.error("LPC.regGet: iopl() disable failed")
            raise
