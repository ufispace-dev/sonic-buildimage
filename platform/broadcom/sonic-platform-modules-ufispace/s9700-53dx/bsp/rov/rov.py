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

import subprocess

from bsp.common.logger import Logger
        
class ROVController:
    
    I2C_ADDR = 0x76
    I2C_BUS = 4
    ROV_OUTPUT_REG = 0x8b
    ROV_CONFIG_REG = 0x21    
    
    #VDDC Voltage 0.82V 0.82V 0.76V 0.78V 0.80V 0.84V 0.86V 0.88V
    ROV_CONFIG = [0x73, 0x73, 0x67, 0x6B, 0x6F, 0x77, 0x7B, 0x7F]
    
    #i2cget -y 4 0x76 0x8b
    ROV_READ_CMD = "i2cget -y {} {} {}"
    #i2cset -y 4 0x76 0x21 0x73
    ROV_WRITE_CMD = "i2cset -y {} {} {} {} w"    
            
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
    
    def _run_i2c_cmd(self, cmd):
        retcode, output = subprocess.getstatusoutput(cmd)
        return retcode, output
    
    def _vid_to_volt_str(self, vid):
        volt = (vid - 1)*0.005 + 0.25
        #return str
        return "{0:.3f}V".format(volt)
    
    def get_rov_config(self):
        cmd = self.ROV_READ_CMD.format(self.I2C_BUS, 
                                       self.I2C_ADDR, 
                                       self.ROV_CONFIG_REG)
        retcode, output = self._run_i2c_cmd(cmd)
        if retcode != 0:
            self.logger.error("get_rov_config failed, cmd={}, output={}".format(cmd, output))
            return 0
        
        return int(output, 16)
    
    def set_rov_config(self, rov_stamp):
        cmd = self.ROV_WRITE_CMD.format(self.I2C_BUS, 
                                        self.I2C_ADDR, 
                                        self.ROV_CONFIG_REG,
                                        self.ROV_CONFIG[rov_stamp])        
        retcode, output = self._run_i2c_cmd(cmd)
        if retcode != 0:
            self.logger.error("set_rov_config failed, cmd={}, output={}".format(cmd, output))
            return False
        else:
            self.logger.info("set_rov_config addr=0x{:02X}, rov_stamp=0x{:02X}, rov_voltage={}".format(
            self.I2C_ADDR, rov_stamp, self._vid_to_volt_str(self.ROV_CONFIG[rov_stamp])))
        return True
    
    def get_rov_output(self):
        cmd = self.ROV_READ_CMD.format(self.I2C_BUS, 
                                       self.I2C_ADDR, 
                                       self.ROV_OUTPUT_REG)
        retcode, output = self._run_i2c_cmd(cmd)
        if retcode != 0:
            self.logger.error("get_rov_output failed, cmd={}, output={}".format(cmd, output))
            return 0
        
        return int(output, 16)    