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

import os

from bsp.common.logger import Logger
from bsp.protocol.lpc import LPC, LPCDevType
from bsp.cpld.cpld_reg import CPLDMBReg

class BrdIDUtility:

    PATH_DIR = "/tmp/bsp/"
    PATH_BOARD_ID = PATH_DIR + "board_id"
    
    MASK_MODEL_ID  = 0b01110000
    MASK_HW_REV    = 0b00001100
    MASK_BUILD_REV = 0b00000011
    MASK_BUILD_REV_EXT = 0b10000000
    
    #EXT_BOARD_ID = 0b1110
    
    BOARD_ID_MAP = {0b000: "Reserved",
                    0b001: "Reserved",
                    0b010: "Apollo NCP1-1 40+13P",
                    0b011: "Reserved",
                    0b100: "Apollo NCP2-1 10+13P",
                    0b101: "Reserved",
                    0b110: "Reserved",
                    0b111: "Apollo NCF 48P",
                    }    

    #EXT_BOARD_ID_MAP = {}

    HARDWARE_REV_MAP = {0b00: "Proto",
                        0b01: "Alpha",
                        0b10: "Beta",
                        0b11: "PVT"}

    BUILD_REV_MAP = {0b000: "A1",
                     0b001: "A2",
                     0b010: "A3",
                     0b011: "A4",
                     0b100: "A5",
                     0b101: "A6",
                     0b110: "A7",
                     0b111: "A8"
                     }
        
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.lpc = LPC()
    
    # get bit shift from mask
    def _get_shift(self, reg_mask):
        mask_one = 1
        
        for i in range(8):
            if reg_mask & mask_one == 1:
                return i
            else:
                reg_mask >>= 1
        
        # not found
        return -1
       
    def get_board_id(self):
        path_dir = self.PATH_DIR     
        path_board_id = self.PATH_BOARD_ID
        try:            
            if os.path.exists(path_board_id):
                #board_id file exists
                with open(path_board_id, "r") as f:
                    # read content
                    content = f.read()                    
                    board_id = int(content.strip(), 0)                    
            else:
                #read board id from LPC                       
                board_id = self.lpc.regGet(LPCDevType.CPLD_ON_MAIN_BOARD,
                                       CPLDMBReg.REG_BRD_ID)
                
                #create board_id parent directories
                os.makedirs(os.path.dirname(path_dir), exist_ok=True)
                
                #write to board_id file
                if os.path.exists(path_dir):
                    with open(path_board_id, "w") as f:
                        f.write(str(board_id))                    
                else:
                    self.logger.error("create board_id file failed: path={}".format(path_board_id))
                    return -1
                                
            return board_id
        except Exception as e:
            self.logger.error(e)
            raise

    def get_model_id(self, board_id): 
        return (board_id & self.MASK_MODEL_ID) >> self._get_shift(self.MASK_MODEL_ID)
    
    def get_hw_rev(self, board_id):
        return (board_id & self.MASK_HW_REV) >> self._get_shift(self.MASK_HW_REV)
    
    def get_build_rev(self, board_id):
        #bit[7], bit[1], bit[0]
        return  ((board_id & self.MASK_BUILD_REV) >> self._get_shift(self.MASK_BUILD_REV)) | \
                (((board_id & self.MASK_BUILD_REV_EXT) >> self._get_shift(self.MASK_BUILD_REV_EXT)) << 2)

    def get_model_id_str(self, model_id):
        if model_id in self.BOARD_ID_MAP.keys():
            model_id_str = self.BOARD_ID_MAP[model_id]
        else:
            model_id_str = "unknown" 
        return model_id_str
    
    def get_hw_rev_str(self, hw_rev):
        if hw_rev in self.HARDWARE_REV_MAP.keys():
            hw_rev_str = self.HARDWARE_REV_MAP[hw_rev]
        else:
            hw_rev_str = "unknown" 
        return hw_rev_str
    
    def get_build_rev_str(self, build_rev):
        if build_rev in self.BUILD_REV_MAP.keys():
            build_rev_str = self.BUILD_REV_MAP[build_rev]
        else:
            build_rev_str = "unknown" 
        return build_rev_str
    