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
from bsp.gpio.ioexp import IOExpander
from bsp.const.const import USBMux, BID
from bsp.utility.board_id_utility import BrdIDUtility

class USBMuxUtility:

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.ioexp = IOExpander()        
        self.brd_id_util = BrdIDUtility()
        self.board_id = self.brd_id_util.get_board_id()
        
    def set_usb_mux(self, source):
        try:
            if source not in [USBMux.CPU, USBMux.BMC]:
                raise ValueError("invalid usb source {0}, range is 0-1".format(source))                
            if (self.board_id & BID.BUILD_REV_MASK) >= BID.NCP1_1_BETA:
                raise ValueError("USB Mux is not supported since BETA".format(source))
            
            self.ioexp.set_usb_mux(source)
        except Exception as e:
            self.logger.error("set_usb_mux {0} failed, error: {1}".format(source, e))
