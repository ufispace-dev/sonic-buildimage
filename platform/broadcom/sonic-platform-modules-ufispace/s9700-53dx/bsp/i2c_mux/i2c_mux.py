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
import sys
import subprocess

from bsp.common.logger import Logger
from bsp.const.const import BID
from bsp.utility.sysfs_utility import SysfsUtility
from bsp.utility.board_id_utility import BrdIDUtility

class PCA954x:

    def __init__(self, name, address, bus, chnl_bus):
        self.name = self.NAME + " " + name
        self.address = address
        self.bus = bus
        self.chnl_bus = chnl_bus

class PCA9548(PCA954x):

    NAME = "pca9548"
    CHANNEL_MAX = 8

class PCA9546(PCA954x):

    NAME = "pca9546"
    CHANNEL_MAX = 4

class I2CMux:

    # MUX Addr
    I2C_ADDR_9548_ROOT_GB = 0x75
    I2C_ADDR_9548_ROOT_QSFP = 0x72
    I2C_ADDR_9548_ROOT_SFP_CPLD = 0x73
    I2C_ADDR_9548_CHILD_GB = 0x76
    I2C_ADDR_9548_CHILD_QSFP = 0x76
    I2C_ADDR_9548_CHILD_QSFPDD = 0x76
    I2C_ADDR_9548_CHILD_QSFPDDBOARD = 0x71

    BUS_I801 = 0

    ATTR_IDLE_STATE = "idle_state"
    IDLE_STATE_DISCONNECT = -2
    IDLE_STATE_AS_IS = -1
    
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.sysfs_util = SysfsUtility()
        self.brd_id_util = BrdIDUtility()
        #Global Mux Alias
        board_id = self.brd_id_util.get_board_id()

        if board_id == BID.NCP1_1_PROTO:

            self.MUXs = {
                # MUX PCA9548 ROOT Gearbox
                "9548_ROOT_GB": PCA9548("ROOT_GB", 
                                  self.I2C_ADDR_9548_ROOT_GB, 
                                  self.BUS_I801, 
                                  [i for i in range(1, 9)]),
                # MUX PCA9548 ROOT QSFP, QSFPDD
                "9548_ROOT_QSFP": PCA9548("ROOT_QSFP", 
                                  self.I2C_ADDR_9548_ROOT_QSFP, 
                                  self.BUS_I801, 
                                  [i for i in range(9, 17)]),
                # MUX PCA9548#2 SFP, CPLD, etc
                "9548_ROOT_SFP_CPLD": PCA9548("ROOT_SFP_CPLD", 
                                  self.I2C_ADDR_9548_ROOT_SFP_CPLD, 
                                  self.BUS_I801, 
                                  [i for i in range(17, 25)]),
                # MUX PCA9548#3 Gearbox #1-#8
                "9548_CHILD_GB0": PCA9548("CHILD_GB0", 
                                  self.I2C_ADDR_9548_CHILD_GB, 
                                  7, 
                                  [i for i in range(25, 33)]),
                # MUX PCA9548 Gearbox #9-#10
                "9548_CHILD_GB1": PCA9548("CHILD_GB1", 
                                  self.I2C_ADDR_9548_CHILD_GB, 
                                  8, 
                                  [i for i in range(33, 41)]),
                # MUX PCA9548 QSFP 0-7               
                "9548_CHILD_QSFP0": PCA9548("CHILD_QSFP0", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  9, 
                                  [i for i in range(41, 49)]),
                # MUX PCA9548 QSFP 8-15
                "9548_CHILD_QSFP1": PCA9548("CHILD_QSFP1", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  10, 
                                  [i for i in range(49, 57)]),
                # MUX PCA9548 QSFP 16-23
                "9548_CHILD_QSFP2": PCA9548("CHILD_QSFP2", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  11, 
                                  [i for i in range(57, 65)]),
                # MUX PCA9548 QSFP 24-31
                "9548_CHILD_QSFP3": PCA9548("CHILD_QSFP3", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  12, 
                                  [i for i in range(65, 73)]),
                # MUX PCA9548 QSFP 32-39
                "9548_CHILD_QSFP4": PCA9548("CHILD_QSFP4", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  13, 
                                  [i for i in range(73, 81)]),
                # MUX PCA9548 QSFPDD 4-7 & DD Board
                "9548_CHILD_QSFPDD0": PCA9548("CHILD_QSFPDD0", 
                                  self.I2C_ADDR_9548_CHILD_QSFPDD, 
                                  15, 
                                  [i for i in range(81, 89)]),
                # MUX PCA9548 QSFPDD 0-3
                "9548_CHILD_QSFPDDBOARD": PCA9548("CHILD_QSFPDDBOARD", 
                                  self.I2C_ADDR_9548_CHILD_QSFPDDBOARD, 
                                  81, 
                                  [i for i in range(89, 97)]),
                # MUX PCA9548 QSFPDD 8-12
                "9548_CHILD_QSFPDD1": PCA9548("CHILD_QSFPDD1", 
                                  self.I2C_ADDR_9548_CHILD_QSFPDD, 
                                  16, 
                                  [i for i in range(97, 105)]),
            }            
            
            self.MUX_ORDER = ["9548_ROOT_GB", "9548_ROOT_QSFP", "9548_ROOT_SFP_CPLD",
                              "9548_CHILD_GB0", "9548_CHILD_GB1",
                              "9548_CHILD_QSFP0", "9548_CHILD_QSFP1", "9548_CHILD_QSFP2",
                              "9548_CHILD_QSFP3", "9548_CHILD_QSFP4",
                              "9548_CHILD_QSFPDD0", "9548_CHILD_QSFPDDBOARD", "9548_CHILD_QSFPDD1"
                              ]
        elif (board_id & BID.BUILD_REV_MASK) >= BID.NCP1_1_ALPHA:
            
            self.MUXs = {
                # MUX PCA9548 ROOT Gearbox
                "9548_ROOT_GB": PCA9548("ROOT_GB", 
                                  self.I2C_ADDR_9548_ROOT_GB, 
                                  self.BUS_I801, 
                                  [i for i in range(1, 9)]),
                # MUX PCA9548 ROOT QSFP, QSFPDD
                "9548_ROOT_QSFP": PCA9548("ROOT_QSFP", 
                                  self.I2C_ADDR_9548_ROOT_QSFP, 
                                  self.BUS_I801, 
                                  [i for i in range(9, 17)]),
                # MUX PCA9548#2 SFP, CPLD, etc
                "9548_ROOT_SFP_CPLD": PCA9548("ROOT_SFP_CPLD", 
                                  self.I2C_ADDR_9548_ROOT_SFP_CPLD, 
                                  self.BUS_I801, 
                                  [i for i in range(17, 25)]),                
                # MUX PCA9548 QSFP 0-7               
                "9548_CHILD_QSFP0": PCA9548("CHILD_QSFP0", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  9, 
                                  [i for i in range(25, 33)]),
                # MUX PCA9548 QSFP 8-15
                "9548_CHILD_QSFP1": PCA9548("CHILD_QSFP1", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  10, 
                                  [i for i in range(33, 41)]),
                # MUX PCA9548 QSFP 16-23
                "9548_CHILD_QSFP2": PCA9548("CHILD_QSFP2", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  11, 
                                  [i for i in range(41, 49)]),
                # MUX PCA9548 QSFP 24-31
                "9548_CHILD_QSFP3": PCA9548("CHILD_QSFP3", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  12, 
                                  [i for i in range(49, 57)]),
                # MUX PCA9548 QSFP 32-39
                "9548_CHILD_QSFP4": PCA9548("CHILD_QSFP4", 
                                  self.I2C_ADDR_9548_CHILD_QSFP, 
                                  13, 
                                  [i for i in range(57, 65)]),
                # MUX PCA9548 QSFPDD 4-7 & DD Board
                "9548_CHILD_QSFPDD0": PCA9548("CHILD_QSFPDD0", 
                                  self.I2C_ADDR_9548_CHILD_QSFPDD, 
                                  15, 
                                  [i for i in range(65, 73)]),                
                # MUX PCA9548 QSFPDD 8-12
                "9548_CHILD_QSFPDD1": PCA9548("CHILD_QSFPDD1", 
                                  self.I2C_ADDR_9548_CHILD_QSFPDD, 
                                  16, 
                                  [i for i in range(73, 81)]),
            }

            self.MUX_ORDER = ["9548_ROOT_GB", "9548_ROOT_QSFP", "9548_ROOT_SFP_CPLD",
                              "9548_CHILD_QSFP0", "9548_CHILD_QSFP1", "9548_CHILD_QSFP2",
                              "9548_CHILD_QSFP3", "9548_CHILD_QSFP4",
                              "9548_CHILD_QSFPDD0", "9548_CHILD_QSFPDD1"
                              ]
        else:
            self.logger.error("[I2C Mux] Invalid Board ID:" + str(board_id))
            sys.exit("[I2C Mux] Invalid Board ID:" + str(board_id))

    def _check_mux(self, bus, addr):
        #check IOExpander exists
        retcode, _ = subprocess.getstatusoutput("i2cget -f -y {} {}".format(bus, addr))
        return retcode

    def _create_sysfs(self, mux):
        try:
            #path of mux
            mux_path = self.sysfs_util.get_bus_path(mux.bus)
            
            #path of mux channel 0
            mux_chnl_path_0 = self.sysfs_util.get_bus_path(mux.chnl_bus[0])            
            
            #check if sysfs already exists
            if os.path.exists(mux_chnl_path_0):
                self.logger.info("[{}] sysfs path already exists: {}".format(mux.name, mux_chnl_path_0))
            else:
                retcode = self._check_mux(mux.bus, mux.address)
                if self._check_mux(mux.bus, mux.address) != 0:
                    self.logger.error("I2C Mux {} (0x{:02X}) access error on bus {}, return code = {} ".format(mux.name,
                                                                                       mux.address,
                                                                                       mux.bus,
                                                                                       retcode))
                    sys.exit()
                #create sysfs            
                else:
                    with open(mux_path + "/" + self.sysfs_util.OP_NEW_DEV, 'w') as f:
                        f.write(mux.NAME + " " + hex(mux.address))
                        self.logger.info("Register {}({}) in sysfs".format(mux.name, mux.address))
                        
                    # set idle_state to -2 if idle_state present
                    idle_state_path = self.sysfs_util.get_sysfs_path(mux.bus, mux.address, self.ATTR_IDLE_STATE)
                    if os.path.exists(idle_state_path):
                        with open(idle_state_path, 'w') as f:
                            f.write(str(self.IDLE_STATE_DISCONNECT))
                            self.logger.info("set {} to {}".format(idle_state_path, self.IDLE_STATE_DISCONNECT))
                            
        except Exception as e:
            self.logger.error("Register MUX " + mux.name + " to sysfs fail, error: ", str(e))
            raise

    def _remove_sysfs(self, mux):
        try:
            i2c_bus = mux.bus
            i2c_addr = mux.address

            path_dev = self.sysfs_util.get_sysfs_path(i2c_bus, i2c_addr)
            path_del = self.sysfs_util.get_del_dev_path(i2c_bus)
            if os.path.exists(path_dev):
                with open(path_del, 'w') as f:
                    f.write(hex(i2c_addr))
                    self.logger.info("Un-register device {} on bus {}".format(hex(i2c_addr), i2c_bus))
        except Exception:
            self.logger.error("Unable to un-register device {} on bus {}".format(hex(i2c_addr), i2c_bus))
            raise

    def init(self):        
        for mux in self.MUX_ORDER:
            try:
                self._create_sysfs(self.MUXs[mux])
            except Exception:                
                raise

    def deinit(self):
        self.MUX_ORDER.reverse()
        for mux in self.MUX_ORDER:
            try:
                self._remove_sysfs(self.MUXs[mux])
            except Exception:                
                raise

    def pre_init(self):
        muxs = ["9548_ROOT_GB", "9548_ROOT_SFP_CPLD", "9548_ROOT_QSFP"]
        
        #check I2C Mux is accessible on bus 0
        for mux in muxs:
            addr = self.MUXs[mux].address
            bus = self.MUXs[mux].bus
            
            retcode, output = subprocess.getstatusoutput("i2cget -f -y {} {}".format(bus, addr))
            if retcode != 0:                
                self.logger.error("I2C Mux[0x{:02X}] access error, return code = {}, output = {} ".format(addr, retcode, output))
                return 1
        
        self.logger.info("[Check Top Mux] Pass")        
        return 0     