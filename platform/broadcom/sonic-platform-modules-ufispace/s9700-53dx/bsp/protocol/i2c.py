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

from smbus import SMBus

from bsp.common.logger import Logger

class I2C_Dev:
        
    def __init__(self, bus, addr):        
        self.bus = bus
        self.addr = addr
        
class I2C:

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
    
    ### SMBus byte access
    
    def read_byte_data(self, i2c_bus, i2c_addr, i2c_reg):
        try:                                                    
            try:                
                bus = SMBus(i2c_bus)
            except:
                raise

            try:
                reg_val = bus.read_byte_data(i2c_addr, i2c_reg)                
            except:
                raise
            finally:
                bus.close()                      
#             
            return reg_val
        except Exception as e:
            self.logger.error("read_byte_data fail, error: " + str(e))
            raise    
    
    def write_byte_data(self, i2c_bus, i2c_addr, i2c_reg, data):
        try:                                                    
            try:                
                bus = SMBus(i2c_bus)
            except:
                raise

            try:
                bus.write_byte_data(i2c_addr, i2c_reg, data)                
            except:
                raise
            finally:
                bus.close()
            
        except Exception as e:
            self.logger.error("write_byte_data fail, error: " + str(e))
    
    ### I2C block access
    
    def read_i2c_block_data(self, i2c_bus, i2c_addr, i2c_reg, data_len=32):
        try:                                                    
            try:                
                bus = SMBus(i2c_bus)
            except:
                raise

            try:
                data_list = bus.read_i2c_block_data(i2c_addr, i2c_reg, data_len)                
            except:
                raise
            finally:
                bus.close()                      
#             
            return data_list
        except Exception as e:
            self.logger.error("read_i2c_block_data fail, error: " + str(e))
            raise
    
    def write_i2c_block_data(self, i2c_bus, i2c_addr, i2c_reg, data):
        try:                                                    
            try:                
                bus = SMBus(i2c_bus)
            except:
                raise

            try:
                bus.write_i2c_block_data(i2c_addr, i2c_reg, data)                
            except:
                raise
            finally:
                bus.close()
            
        except Exception as e:
            self.logger.error("write_i2c_block_data fail, error: " + str(e))
            raise
        
    ### SMBus block access
                        
    def write_block_data(self, i2c_bus, i2c_addr, i2c_reg, data):
        try:                                                    
            try:                
                bus = SMBus(i2c_bus)
            except:
                raise

            try:
                bus.write_block_data(i2c_addr, i2c_reg, data)                
            except:
                raise
            finally:
                bus.close()
            
        except Exception as e:
            self.logger.error("write_block_data fail, error: " + str(e))
            raise    
        
    
    def read_block_data(self, i2c_bus, i2c_addr, i2c_reg):
        try:                                                    
            try:                
                bus = SMBus(i2c_bus)
            except:
                raise

            try:
                data_list = bus.read_block_data(i2c_addr, i2c_reg)                
            except:
                raise
            finally:
                bus.close()                      
#             
            return data_list
        except Exception as e:
            self.logger.error("read_block_data fail, error: " + str(e))
            raise
                    
        
    
