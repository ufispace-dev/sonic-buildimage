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
import os.path

from bsp.common.logger import Logger

class Sensor:
    
    TYPE_ALL = ""
    TYPE_FAN = "Fan"
    TYPE_VOLTAGE = "VSENSE"
    STATUS_OK = "ok"
    
    def __init__(self, name, value, unit, status):
        log = Logger(__name__)
        self.logger = log.getLogger()
        
        self.name = name
        self.value = value
        self.unit = unit
        self.status = status
        
class IPMITool:
    
    IPMI_SDR_LIST_COMMAND = "ipmitool sdr list all"
    IPMI_UARTMUX_COMMAND = "ipmitool raw 0x3c 0x11 0x50 0x1 {}"
    IPMI_UCD_RESET_CMD = "ipmitool raw 0x3c 0x24 0x01 0x00"
    IPMI_LAN = "ipmitool lan print"
    IPMI_BMC_IP = "{} | grep 'IP Address              :' | awk '{{ print $4 }}'".format(IPMI_LAN)
    IPMI_DEV = "/dev/ipmi0"
    
    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
    
    def _parse_sdr(self, sdr_output):        
        sensor_list = []        
        
        lines = sdr_output.split("\n")
        for line in lines:
            columns = line.split("|")            
            name=columns[0].strip()
            value_unit_list = columns[1].strip().split(" ")
            value = value_unit_list[0].strip()
            if len(value_unit_list) > 1:
                unit = value_unit_list[1].strip()
            else:
                unit = ""
            status = columns[2].strip()
            sensor_list.append(Sensor(name, value, unit ,status))
            
        return sensor_list
    
    def _run_ipmitool(self, command):                    
        status, output = subprocess.getstatusoutput(command)
        
        return status, output
        
    def get_sensor(self, keyword=""):
        all_sensor_list = []
        matched_sensor_list = []
        
        try:
            _, output = self._run_ipmitool(self.IPMI_SDR_LIST_COMMAND)            
            all_sensor_list = self._parse_sdr(output)
            
            if keyword:
                for sensor in all_sensor_list:
                    if keyword in sensor.name:
                        matched_sensor_list.append(sensor)
            else:
                matched_sensor_list = all_sensor_list               
            
        except Exception as e:
            self.logger.error("get_sensor() fail, error: " + str(e))
            raise        
            
        return matched_sensor_list
    
    def get_fan_sensors(self):        
        keyword = Sensor.TYPE_FAN
        matched_sensors = self.get_sensor(keyword)
        
        return matched_sensors
    
    def get_fan_sensor(self, fan_num):        
        keyword = Sensor.TYPE_FAN + str(fan_num)
        matched_sensors = self.get_sensor(keyword)
        
        return matched_sensors       
    
    def is_ipmidev_exist(self):        
        return os.path.exists(self.IPMI_DEV)

    def set_uart_mux(self, source):
        try:
            cmd = self.IPMI_UARTMUX_COMMAND.format(hex(source))
            output = self._run_ipmitool(cmd)
        except Exception as e:
            self.logger.error("set_uart_mux() fail, cmd={}, error={}".format(cmd, str(e)))
            raise        
            
        return output    

    def reset_ucd(self):       
        cmd = self.IPMI_UCD_RESET_CMD
        try:            
            self._run_ipmitool(cmd)
        except Exception as e:
            self.logger.error("reset_ucd() fail, cmd={}, error={}".format(cmd, str(e)))
            raise
    
    def get_bmc_ip(self):
        cmd = self.IPMI_BMC_IP
        try:            
            retcode, output = self._run_ipmitool(cmd)
            if retcode != 0:
                self.logger.error("get_bmc_ip() fail, retcode={}, output={}".format(cmd, retcode, output))
                return ""
            else:
                return output                
        except Exception as e:
            self.logger.error("get_bmc_ip() fail, cmd={}, error={}".format(cmd, str(e)))
            raise
            
    def init(self):
        pass

    def deinit(self):
        pass
