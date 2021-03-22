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
from bsp.gpio.ioexp import IOExpander
from bsp.cpld.cpld import CPLD
from bsp.const.const import CPLDConst
from bsp.protocol.lpc import LPC
from bsp.protocol.lpc import LPCDevType

class INTRUtility:
        
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.ioexp = IOExpander()
        self.cpld = CPLD()   
        self.lpc = LPC()
        self.ioexp = IOExpander()
        
        #GPIO REGs
        self.ALERT_GPIO_REG = 0x1
        #I2C Alert REGs
        self.ALERT_STATUS_REG = 0x0
        self.ALERT_DIS_REG = 0x11
        
    def init_i2c_alert(self):
        i2c_detect_cmd = "i2cdetect -y 0"
        
        #i2cdetect -y 0
        retcode, _ = subprocess.getstatusoutput(i2c_detect_cmd)
        if retcode != 0:                
            self.logger.error("i2c command error: {}".format(i2c_detect_cmd))
            
        #Set pin function to alert mode on CPU
        #./ioset 0x501 0xf7
        #IO_x500[11]  SMBALERT_N_GPIO11
        #0/Alert mode,1/GPIO mode
        #Default is 0
        regVal = self.lpc.regGet(LPCDevType.BDE_GPIO_ON_CPU_BOARD,
                        self.ALERT_GPIO_REG)
        self.lpc.regSet(LPCDevType.BDE_GPIO_ON_CPU_BOARD,
                        self.ALERT_GPIO_REG,
                        regVal & 0xF7)
        
        #Enable alert function on CPU
        #./ioset 0xf011 0x0
        #IO_xF011[2]  SMBALERT_DIS
        #0/Enable Alert, 1/Disable alert
        #Default is 1
        regVal = self.lpc.regGet(LPCDevType.CPU_I2C_ALERT,
                        self.ALERT_DIS_REG)       
        self.lpc.regSet(LPCDevType.CPU_I2C_ALERT,
                        self.ALERT_DIS_REG,
                        regVal & 0xFB)
    
    def deinit_i2c_alert(self):
        regVal = self.lpc.regGet(LPCDevType.CPU_I2C_ALERT,
                        self.ALERT_DIS_REG)        
        self.lpc.regSet(LPCDevType.CPU_I2C_ALERT,
                        self.ALERT_DIS_REG,
                        regVal | 0x04)
    
    def get_alert_gpio(self):
        regVal = self.lpc.regGet(LPCDevType.BDE_GPIO_ON_CPU_BOARD,
                        self.ALERT_GPIO_REG)        
        return (regVal >> 3) & 1
    
    def get_alert_dis(self):
        regVal = self.lpc.regGet(LPCDevType.CPU_I2C_ALERT,
                        self.ALERT_DIS_REG)        
        return (regVal >> 2) & 1
    
    def get_alert_sts(self):
        regVal = self.lpc.regGet(LPCDevType.CPU_I2C_ALERT,
                        self.ALERT_STATUS_REG)        
        return (regVal >> 5) & 1
    
    def clear_i2c_alert(self):
        intr_reg = "9539_HOST_GPIO_I2C"
        cpu_gpio_reg = "9539_CPU_I2C"
        
        #clear alert on ioexpander
        #i2cdump -y 0 0x74
        reg_vals = self.ioexp.dump_reg(intr_reg)
        self.logger.info("clear_i2c_alert() intr_reg_vals={}".format(reg_vals))
        
        #i2cdump -y 0 0x77
        reg_vals = self.ioexp.dump_reg(cpu_gpio_reg)
        self.logger.info("clear_i2c_alert() cpu_gpio_reg_vals={}".format(reg_vals))
        
        #clear i2c alert status on CPU
        #./ioset 0xf000 0x60
        self.lpc.regSet(LPCDevType.CPU_I2C_ALERT,
                        self.ALERT_STATUS_REG,
                        0x60)
        
    def get_cpld_to_cpu_intr(self):
        cpld_intr_name = ["op2", "cpld_1_2", "cpld_3", "cpld_4", "cpld_5", "j2"]
        cpld_intr = {}
        try:
            cpld_intr_val = self.ioexp.get_cpld_to_cpu_intr()
            for i in range(len(cpld_intr_val)):
                cpld_intr[cpld_intr_name[i]] = cpld_intr_val[i]
            
            return cpld_intr    
                         
        except Exception as e:
            self.logger.error("get_cpld_to_cpu_intr failed, error: {}".format(e))

    def get_all_cpld_intr(self):
        cpld_name = "cpld_"
        all_cpld_intr = {}
        try:
            for i in range(CPLDConst.CPLD_MAX):
                cpld_intr = self.get_cpld_intr(i)
                all_cpld_intr[cpld_name+str(i+1)] = cpld_intr
            
            return all_cpld_intr
        except Exception as e:
            self.logger.error("get_cpld_intr failed, error: {}".format(e))

    def get_cpld_intr(self, cpld_num):
        cpld_intr_name = ["port_intr", "gearbox", "usb", "port_presence", 
                          "psu0", "psu1", "pex8724", "cs4227",
                          "retimer"]
        cpld_intr = {}
        try:
            intr_reg = self.cpld.get_intr_reg(cpld_num, 0)

            if cpld_num == CPLDConst.CPLD_1:
                intr_reg_2 = self.cpld.get_intr_reg(cpld_num, 1)
                
                for i in range(8):
                    cpld_intr[cpld_intr_name[i]] = intr_reg >> i & 0b1

                cpld_intr[cpld_intr_name[8]] = intr_reg_2 & 0b1
            else:
                cpld_intr[cpld_intr_name[0]] = intr_reg >> 0 & 0b1
                cpld_intr[cpld_intr_name[3]] = intr_reg >> 3 & 0b1
            
            return cpld_intr
                     
        except Exception as e:
            self.logger.error("get_cpld_intr failed, error: {}".format(e))

    def clear_all_intr(self):
        try:
            for i in range(CPLDConst.CPLD_MAX):
                self.get_cpld_intr(i)
            self.clear_i2c_alert()
                       
        except Exception as e:
            self.logger.error("clear_all_intr failed, error: {}".format(e))

    def get_gbox_intr(self):
        gbox_name = "gearbox"
        gbox_intr = {}
        gbox_max_1 = 8
        gbox_max_2 = 2
        
        try:
            reg1, reg2 = self.cpld.gbox_get_intr()
            
            for i in range(gbox_max_1):
                gbox_intr[gbox_name + "_" + str(i)] = reg1 >> i & 0b1
                                
            for i in range(gbox_max_2):
                gbox_intr[gbox_name + "_" + str(gbox_max_1 + i)] = reg2 >> i & 0b1
                
            return gbox_intr
        except Exception as e:            
            self.logger.error("get_gbox_intr failed, error: {}".format(e))
    
    def get_retimer_intr(self):
        retimer_name = "retimer"
        retimer_intr = {}
        retimer_max = 5
        
        try:  
            reg = self.cpld.retimer_get_intr()
            
            for i in range(retimer_max):
                retimer_intr[retimer_name + "_" + str(i)] = reg >> i & 0b1
                
            return retimer_intr
        except Exception as e:
            self.logger.error("get_retimer_intr failed, error: {}".format(e)) 