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

class SysfsUtility:

    PATH_SYS_I2C_DEVICES = "/sys/bus/i2c/devices"
    PATH_SYS_I2C_BUS = "/sys/bus/i2c/devices/i2c-{}"
    PATH_SYS_I2C_BUS_OP = "/sys/bus/i2c/devices/i2c-{}/{}"
    PATH_SYS_I2C_DEV = "/sys/bus/i2c/devices/{}-{}"
    PATH_SYS_I2C_DEV_ATTR = "/sys/bus/i2c/devices/{}-{}/{}"
    PATH_SYS_GPIO = "/sys/class/gpio"
    PATH_SYS_GPIO_N = "/sys/class/gpio/gpio{}"
    PATH_SYS_GPIO_VALUE = "/sys/class/gpio/gpio{}/value"
    
    OP_NEW_DEV = "new_device"
    OP_DEL_DEV = "delete_device"
    
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()          
        
    def get_bus_path(self, bus, sysfs_op=""):
        if sysfs_op == "":
            return self.PATH_SYS_I2C_BUS.format(str(bus))
        else:
            return self.PATH_SYS_I2C_BUS_OP.format(str(bus), sysfs_op)
    
    def get_new_dev_path(self, bus):
        return self.get_bus_path(bus, self.OP_NEW_DEV)
        
    def get_del_dev_path(self, bus):
        return self.get_bus_path(bus, self.OP_DEL_DEV)    
        
    def get_sysfs_path(self, bus, addr, attr=""):
        if attr == "":            
            return self.PATH_SYS_I2C_DEV.format(str(bus), hex(addr)[2:].zfill(4))
        else:
            return self.PATH_SYS_I2C_DEV_ATTR.format(str(bus), hex(addr)[2:].zfill(4), attr)
    
    def get_gpio_root_path(self):
        return self.PATH_SYS_GPIO
                         
    def get_gpio_path(self, gpio_num):
        return self.PATH_SYS_GPIO_N.format(gpio_num)
    
    def get_gpio_val_path(self, gpio_num):
        return self.PATH_SYS_GPIO_VALUE.format(gpio_num)
