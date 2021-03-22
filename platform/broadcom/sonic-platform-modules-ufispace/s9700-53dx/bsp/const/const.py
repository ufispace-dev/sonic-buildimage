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

from enum import IntEnum

class SFP(IntEnum):    
    MAX_PORT = 2
    
    UNDETECTED = 0
    DETECTED = 1
    
    SFP0 = 0
    SFP1 = 1
    
    ENABLED = 0
    DISABLED = 1

class QSFP(IntEnum):
    MAX_PORT = 40
     
class QSFPDD(IntEnum):
    MAX_PORT = 13
    LED_MASK_RED = 0b0001
    LED_MASK_GREEN  = 0b0010    
    LED_MASK_BLUE   = 0b0100
    LED_MASK_BLINK  = 0b1000
    
class PortRate(IntEnum):
    Rate_1G = 0
    Rate_10G = 1

class PortStatus(IntEnum):
    ENABLED = 0
    DISABLED = 1

    PORT_PRESENCE = 0
    PORT_ABSENCE = 1
    
    INTERRUPTED = 0
    RESET = 0
    NO_RESET = 1

class PSU(IntEnum):    
    PSU0 = 0
    PSU1 = 1  
    
    MAX_PSU = 2
        
class PSUStatus(IntEnum):    
    PRESENCE = 0
    ABSENCE = 1
    
    POWER_FAIL = 0
    POWER_OK = 1        
        
class Led(IntEnum):
    SYSTEM = 0    
    FAN = 1
    PSU0 = 2
    PSU1 = 3    

    STATUS_OFF = 0
    STATUS_ON = 1

    COLOR_OFF = 0
    COLOR_YELLOW = 1    
    COLOR_RED = 1
    COLOR_GREEN = 2        
    COLOR_BLUE = 3
    COLOR_MAX = 4

    BLINK_STATUS_SOLID = 0
    BLINK_STATUS_BLINKING = 1
    BLINK_STATUS_MAX = 2 
    
    BEACON_NORMAL = 0
    BEACON_TEST = 1
    BEACON_MAX = 255

    MASK_COLOR = 0b0001
    MASK_BLINK = 0b0100
    MASK_ONOFF = 0b1000
    
class CPLDConst(IntEnum):
    LOC_MB = 0
    LOC_CPU = 1

    UART_SOURCE_CPU = 0
    UART_SOURCE_BMC = 1
    
    CPLD_1 = 0
    CPLD_2 = 1
    CPLD_3 = 2
    CPLD_4 = 3
    CPLD_5 = 4
    CPLD_MAX = 5

class UARTMux(IntEnum):    
    CPU = 0
    BMC = 1    

class UARTInterface(IntEnum):    
    RJ45 = 0
    MICRO_USB = 1
            
class USBMux(IntEnum):    
    CPU = 0
    BMC = 1    
    
class CPLDSource(IntEnum):    
    CPU = 0
    MB = 1
      
class LPMode(IntEnum):
    DISABLE = 0
    ENABLE = 1
    
class DataType(IntEnum):
    INT = 0    
    
class BMC(IntEnum):    
    PRESENCE = 0
    ABSENCE = 1    

class BID(IntEnum):
    NCP1_1_PROTO = 32
    NCP1_1_ALPHA = 36
    NCP1_1_BETA  = 40
    #MODEL_ID_BIT  = 0b01110000
    #HW_REV_BIT    = 0b00001100
    #BUILD_REV_BIT = 0b00000011
    BUILD_REV_MASK = 0b01111100

class DevType(IntEnum):
    J2 = 0
    GEARBOX = 1
    RETIMER = 2
    CS4227 = 3
    OP2 = 4
    PEX8724 = 5    
    OP2_CRST = 6
    OP2_PERST = 7
    OP2_SRST = 8
    DEV_MAX = 9

class ResetStatus(IntEnum):
    RESET = 0
    UNSET = 1

class Gearbox(IntEnum):
    GBOX_MAX = 10
    
class Retimer(IntEnum):
    RETIMER_MAX = 5