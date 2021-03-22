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
import time

from bsp.common.logger import Logger
from bsp.const.const import BID
from bsp.utility.sysfs_utility import SysfsUtility
from bsp.utility.board_id_utility import BrdIDUtility

class PCA953x:

    def __init__(self, dev_info, bus_num):
        self.name = dev_info["name"]
        self.address = dev_info["address"]
        self.bus_num = bus_num
        self.pins = dev_info["pins"]
        self.init_cfg = dev_info["init_cfg"]

class PCA9555(PCA953x):

    NAME = "pca9555"

class PCA9535(PCA953x):

    NAME = "pca9535"

class PCA9539(PCA953x):

    NAME = "pca9539"

class IOExpander:

    APOLLO_PROTO_IOExpanders_Order_List = ['9539_HOST_GPIO_I2C', '9539_SYS_LED', '9555_BOARD_ID', '9539_VOL_MARGIN', '9539_CPU_I2C']
    APOLLO_ALPHA_IOExpanders_Order_List = ['9539_HOST_GPIO_I2C', '9539_SYS_LED', '9555_BOARD_ID', '9539_VOL_MARGIN', '9539_CPU_I2C', '9555_BEACON_LED']
    APOLLO_BETA_IOExpanders_Order_List = ['9539_HOST_GPIO_I2C', '9555_BEACON_LED', '9555_BOARD_ID', '9539_VOL_MARGIN', '9539_CPU_I2C']

    def __init__(self):
        log = Logger(__name__)
        self.logger = log.getLogger()
        self.sysfs_util = SysfsUtility()
        self.brd_id_util = BrdIDUtility()

        GPIO_BASE = 511
        self.APOLLO_IOExpanders = {
            "9539_HOST_GPIO_I2C": {
                "name": "pca9539_HOST_GPIO_I2C", "address": 0x74, "parent": None, "channel": None, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE,    "direction": "out", "value": 1, "desc": "IO_1.7 I210_RST_L"},           # gpio511 
                    {"gpio": GPIO_BASE-1,  "direction": "out", "value": 1, "desc": "IO_1.6 I210_PE_RST_L"},        # gpio510  
                    {"gpio": GPIO_BASE-2,  "direction": "in"             , "desc": "IO_1.5 OP2_INT_L"},            # gpio509 
                    {"gpio": GPIO_BASE-3,  "direction": "in"             , "desc": "IO_1.4 CPLD01_TO_CPU_INT_L"},  # gpio508 
                    {"gpio": GPIO_BASE-4,  "direction": "in"             , "desc": "IO_1.3 CPLD2_TO_CPU_INT_L"},   # gpio507 
                    {"gpio": GPIO_BASE-5,  "direction": "in"             , "desc": "IO_1.2 CPLD3_TO_CPU_INT_L"},   # gpio506 
                    {"gpio": GPIO_BASE-6,  "direction": "in"             , "desc": "IO_1.1 CPLD4_TO_CPU_INT_L"},   # gpio505 
                    {"gpio": GPIO_BASE-7,  "direction": "in"             , "desc": "IO_1.0 J2_INT_L"},             # gpio504
                    {"gpio": GPIO_BASE-8,  "direction": "in"             , "desc": "IO_0.7 8V19N474_INT"},         # gpio503
                    {"gpio": GPIO_BASE-9,  "direction": "in"             , "desc": "IO_0.6 TP112012"},             # gpio502
                    {"gpio": GPIO_BASE-10, "direction": "out", "value": 0, "desc": "IO_0.5 UART_MUX_SEL"},         # gpio501
                    {"gpio": GPIO_BASE-11, "direction": "out", "value": 0, "desc": "IO_0.4 USB_MUX_SEL"},          # gpio500
                    {"gpio": GPIO_BASE-12, "direction": "out", "value": 0, "desc": "IO_0.3 HOST_TO_BMC_I2C_GPIO"}, # gpio499  
                    {"gpio": GPIO_BASE-13, "direction": "out", "value": 1, "desc": "IO_0.2 LED_CLR"},              # gpio498  
                    {"gpio": GPIO_BASE-14, "direction": "in"             , "desc": "IO_0.1 J2_PCIE_RST_L"},        # gpio497 
                    {"gpio": GPIO_BASE-15, "direction": "out", "value": 1, "desc": "IO_0.0 9539_TH_RST_L"}         # gpio496 
                ],
                "config_0": 0xc0, "config_1": 0x3f, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x03, "output_port_1": 0xc0
            },
            "9539_SYS_LED": {
                "name": "pca9539_SYS_LED", "address": 0x76, "parent": "9548_ROOT_GB", "channel": 1, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-16, "direction": "in", "desc": "IO_1.7 NONE"},            # gpio495 
                    {"gpio": GPIO_BASE-17, "direction": "in", "desc": "IO_1.6 NONE"},            # gpio494 
                    {"gpio": GPIO_BASE-18, "direction": "in", "desc": "IO_1.5 NONE"},            # gpio493 
                    {"gpio": GPIO_BASE-19, "direction": "in", "desc": "IO_1.4 NONE"},            # gpio492 
                    {"gpio": GPIO_BASE-20, "direction": "in", "desc": "IO_1.3 NONE"},            # gpio491 
                    {"gpio": GPIO_BASE-21, "direction": "in", "desc": "IO_1.2 NONE"},            # gpio490 
                    {"gpio": GPIO_BASE-22, "direction": "in", "desc": "IO_1.1 PSU0_LED_PWR"},    # gpio489 
                    {"gpio": GPIO_BASE-23, "direction": "in", "desc": "IO_1.0 PSU1_LED_PWR"},    # gpio488 
                    {"gpio": GPIO_BASE-24, "direction": "in", "desc": "IO_0.7 SFP+_P16_TX_DIS"}, # gpio487 
                    {"gpio": GPIO_BASE-25, "direction": "in", "desc": "IO_0.6 SFP+_P17_TX_DIS"}, # gpio486 
                    {"gpio": GPIO_BASE-26, "direction": "in", "desc": "IO_0.5 NONE"},            # gpio485 
                    {"gpio": GPIO_BASE-27, "direction": "in", "desc": "IO_0.4 PSU0_LED_Y"},      # gpio484 
                    {"gpio": GPIO_BASE-28, "direction": "in", "desc": "IO_0.3 PSU1_LED_Y"},      # gpio483 
                    {"gpio": GPIO_BASE-29, "direction": "in", "desc": "IO_0.2 FAN_LED_Y"},       # gpio482 
                    {"gpio": GPIO_BASE-30, "direction": "in", "desc": "IO_0.1 FAN_LED_EN"},      # gpio481 
                    {"gpio": GPIO_BASE-31, "direction": "in", "desc": "IO_0.0 SYS_LED_G"}        # gpio480 
                ],
                "config_0": 0xe0, "config_1": 0xfc, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
            "9555_BOARD_ID": {
                "name": "pca9555_BOARD_ID", "address": 0x20, "parent": "9548_ROOT_GB", "channel": 2, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-32, "direction": "in", "desc": "IO_1.7 Board_ID_3"},  # gpio479 
                    {"gpio": GPIO_BASE-33, "direction": "in", "desc": "IO_1.6 Board_ID_2"},  # gpio478 
                    {"gpio": GPIO_BASE-34, "direction": "in", "desc": "IO_1.5 Board_ID_1"},  # gpio477 
                    {"gpio": GPIO_BASE-35, "direction": "in", "desc": "IO_1.4 Board_ID_0"},  # gpio476 
                    {"gpio": GPIO_BASE-36, "direction": "in", "desc": "IO_1.3 HW_REV_1"},    # gpio475 
                    {"gpio": GPIO_BASE-37, "direction": "in", "desc": "IO_1.2 HW_REV_0"},    # gpio474 
                    {"gpio": GPIO_BASE-38, "direction": "in", "desc": "IO_1.1 Build_REV_1"}, # gpio473 
                    {"gpio": GPIO_BASE-39, "direction": "in", "desc": "IO_1.0 Build_REV_0"}, # gpio472 
                    {"gpio": GPIO_BASE-40, "direction": "in", "desc": "IO_0.7 NONE"},        # gpio471 
                    {"gpio": GPIO_BASE-41, "direction": "in", "desc": "IO_0.6 NONE"},        # gpio470 
                    {"gpio": GPIO_BASE-42, "direction": "in", "desc": "IO_0.5 NONE"},        # gpio469 
                    {"gpio": GPIO_BASE-43, "direction": "in", "desc": "IO_0.4 NONE"},        # gpio468 
                    {"gpio": GPIO_BASE-44, "direction": "in", "desc": "IO_0.3 NONE"},        # gpio467 
                    {"gpio": GPIO_BASE-45, "direction": "in", "desc": "IO_0.2 NONE"},        # gpio466 
                    {"gpio": GPIO_BASE-46, "direction": "in", "desc": "IO_0.1 NONE"},        # gpio465 
                    {"gpio": GPIO_BASE-47, "direction": "in", "desc": "IO_0.0 NONE"}         # gpio464
                ],
                "config_0": 0xff, "config_1": 0xff, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
            "9539_VOL_MARGIN": {
                "name": "pca9539_VOL_MARGIN", "address": 0x76, "parent": "9548_ROOT_GB", "channel": 5, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-48, "direction": "in", "desc": "IO_1.7 P1V2_3_Low_Margin"},  # gpio463 
                    {"gpio": GPIO_BASE-49, "direction": "in", "desc": "IO_1.6 P1V2_3_High_Margin"}, # gpio462 
                    {"gpio": GPIO_BASE-50, "direction": "in", "desc": "IO_1.5 P0V9_Low_Margin"},    # gpio461 
                    {"gpio": GPIO_BASE-51, "direction": "in", "desc": "IO_1.4 P0V9_High_Margin"},   # gpio460 
                    {"gpio": GPIO_BASE-52, "direction": "in", "desc": "IO_1.3 P0V88_Low_Margin"},   # gpio459 
                    {"gpio": GPIO_BASE-53, "direction": "in", "desc": "IO_1.2 P0V88_High_Margin"},  # gpio458 
                    {"gpio": GPIO_BASE-54, "direction": "in", "desc": "IO_1.1 NI"},                 # gpio457 
                    {"gpio": GPIO_BASE-55, "direction": "in", "desc": "IO_1.0 NI"},                 # gpio456 
                    {"gpio": GPIO_BASE-56, "direction": "in", "desc": "IO_0.7 P2V5_Low_Margin"},    # gpio455 
                    {"gpio": GPIO_BASE-57, "direction": "in", "desc": "IO_0.6 P2V5_High_Margin"},   # gpio454 
                    {"gpio": GPIO_BASE-58, "direction": "in", "desc": "IO_0.5 P1V8_Low_Margin"},    # gpio453 
                    {"gpio": GPIO_BASE-59, "direction": "in", "desc": "IO_0.4 P1V8_High_Margin"},   # gpio452 
                    {"gpio": GPIO_BASE-60, "direction": "in", "desc": "IO_0.3 P1V2_1_Low_Margin"},  # gpio451 
                    {"gpio": GPIO_BASE-61, "direction": "in", "desc": "IO_0.2 P1V2_1_High_Margin"}, # gpio450 
                    {"gpio": GPIO_BASE-62, "direction": "in", "desc": "IO_0.1 P1V2_2_Low_Margin"},  # gpio449 
                    {"gpio": GPIO_BASE-63, "direction": "in", "desc": "IO_0.0 P1V2_2_High_Margin"}  # gpio448 
                ],
                "config_0": 0x0, "config_1": 0x03, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
            "9539_CPU_I2C": {
                "name": "pca9539_CPU_I2C", "address": 0x77, "parent": None, "channel": None, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-64, "direction": "in", "desc": "IO_1.7"}, # gpio447 
                    {"gpio": GPIO_BASE-65, "direction": "in", "desc": "IO_1.6"}, # gpio446 
                    {"gpio": GPIO_BASE-66, "direction": "in", "desc": "IO_1.5"}, # gpio445 
                    {"gpio": GPIO_BASE-67, "direction": "in", "desc": "IO_1.4"}, # gpio444 
                    {"gpio": GPIO_BASE-68, "direction": "in", "desc": "IO_1.3"}, # gpio443 
                    {"gpio": GPIO_BASE-69, "direction": "in", "desc": "IO_1.2"}, # gpio442 
                    {"gpio": GPIO_BASE-70, "direction": "in", "desc": "IO_1.1"}, # gpio441 
                    {"gpio": GPIO_BASE-71, "direction": "in", "desc": "IO_1.0"}, # gpio440 
                    {"gpio": GPIO_BASE-72, "direction": "in", "desc": "IO_0.7"}, # gpio439 
                    {"gpio": GPIO_BASE-73, "direction": "in", "desc": "IO_0.6"}, # gpio438 
                    {"gpio": GPIO_BASE-74, "direction": "in", "desc": "IO_0.5"}, # gpio437 
                    {"gpio": GPIO_BASE-75, "direction": "in", "desc": "IO_0.4"}, # gpio436 
                    {"gpio": GPIO_BASE-76, "direction": "in", "desc": "IO_0.3"}, # gpio435 
                    {"gpio": GPIO_BASE-77, "direction": "in", "desc": "IO_0.2"}, # gpio434 
                    {"gpio": GPIO_BASE-78, "direction": "in", "desc": "IO_0.1"}, # gpio433 
                    {"gpio": GPIO_BASE-79, "direction": "in", "desc": "IO_0.0"}  # gpio432 
                ],
                "config_0": 0xff, "config_1": 0xff, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
            "9555_BEACON_LED": {
                "name": "pca9555_BEACON_LED", "address": 0x20, "parent": "9548_ROOT_GB", "channel": 6, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-80, "direction": "in"             , "desc": "IO_1.7 NONE"},    # gpio431 
                    {"gpio": GPIO_BASE-81, "direction": "out", "value": 1, "desc": "IO_1.6 7SEG_RG"}, # gpio430 
                    {"gpio": GPIO_BASE-82, "direction": "out", "value": 0, "desc": "IO_1.5 7SEG_RB"}, # gpio429 
                    {"gpio": GPIO_BASE-83, "direction": "out", "value": 0, "desc": "IO_1.4 7SEG_RD"}, # gpio428 
                    {"gpio": GPIO_BASE-84, "direction": "out", "value": 0, "desc": "IO_1.3 7SEG_RF"}, # gpio427 
                    {"gpio": GPIO_BASE-85, "direction": "out", "value": 0, "desc": "IO_1.2 7SEG_RC"}, # gpio426 
                    {"gpio": GPIO_BASE-86, "direction": "out", "value": 0, "desc": "IO_1.1 7SEG_RE"}, # gpio425 
                    {"gpio": GPIO_BASE-87, "direction": "out", "value": 0, "desc": "IO_1.0 7SEG_RA"}, # gpio424 
                    {"gpio": GPIO_BASE-88, "direction": "in"             , "desc": "IO_0.7 NONE"},    # gpio423 
                    {"gpio": GPIO_BASE-89, "direction": "out", "value": 0, "desc": "IO_0.6 7SEG_LA"}, # gpio422 
                    {"gpio": GPIO_BASE-90, "direction": "out", "value": 0, "desc": "IO_0.5 7SEG_LF"}, # gpio421 
                    {"gpio": GPIO_BASE-91, "direction": "out", "value": 1, "desc": "IO_0.4 7SEG_LG"}, # gpio420 
                    {"gpio": GPIO_BASE-92, "direction": "out", "value": 0, "desc": "IO_0.3 7SEG_LD"}, # gpio419 
                    {"gpio": GPIO_BASE-93, "direction": "out", "value": 0, "desc": "IO_0.2 7SEG_LE"}, # gpio418 
                    {"gpio": GPIO_BASE-94, "direction": "out", "value": 0, "desc": "IO_0.1 7SEG_LB"}, # gpio417 
                    {"gpio": GPIO_BASE-95, "direction": "out", "value": 0, "desc": "IO_0.0 7SEG_LC"}  # gpio416 
                ],
                "config_0": 0xff, "config_1": 0xff, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
        }
        
        self.APOLLO_BETA_IOExpanders = {
            "9539_HOST_GPIO_I2C": {
                "name": "pca9539_HOST_GPIO_I2C", "address": 0x74, "parent": None, "channel": None, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE,    "direction": "out", "value": 1, "desc": "IO_1.7 I210_RST_L"},           # gpio511 
                    {"gpio": GPIO_BASE-1,  "direction": "out", "value": 1, "desc": "IO_1.6 I210_PE_RST_L"},        # gpio510 
                    {"gpio": GPIO_BASE-2,  "direction": "in"             , "desc": "IO_1.5 OP2_INT_L"},            # gpio509 
                    {"gpio": GPIO_BASE-3,  "direction": "in"             , "desc": "IO_1.4 CPLD01_TO_CPU_INT_L"},  # gpio508 
                    {"gpio": GPIO_BASE-4,  "direction": "in"             , "desc": "IO_1.3 CPLD2_TO_CPU_INT_L"},   # gpio507 
                    {"gpio": GPIO_BASE-5,  "direction": "in"             , "desc": "IO_1.2 CPLD3_TO_CPU_INT_L"},   # gpio506 
                    {"gpio": GPIO_BASE-6,  "direction": "in"             , "desc": "IO_1.1 CPLD4_TO_CPU_INT_L"},   # gpio505 
                    {"gpio": GPIO_BASE-7,  "direction": "in"             , "desc": "IO_1.0 TH_INT_L"},             # gpio504 
                    {"gpio": GPIO_BASE-8,  "direction": "in"             , "desc": "IO_0.7 8V19N474_INT"},         # gpio503 
                    {"gpio": GPIO_BASE-9,  "direction": "in"             , "desc": "IO_0.6 TP112012"},             # gpio502 
                    {"gpio": GPIO_BASE-10, "direction": "in"             , "desc": "IO_0.5 UART_MUX_SEL"},         # gpio501 
                    {"gpio": GPIO_BASE-11, "direction": "out", "value": 0, "desc": "IO_0.4 USB_MUX_SEL"},          # gpio500 
                    {"gpio": GPIO_BASE-12, "direction": "out", "value": 0, "desc": "IO_0.3 HOST_TO_BMC_I2C_GPIO"}, # gpio499 
                    {"gpio": GPIO_BASE-13, "direction": "out", "value": 1, "desc": "IO_0.2 LED_CLR"},              # gpio498 
                    {"gpio": GPIO_BASE-14, "direction": "in"             , "desc": "IO_0.1 J2_PCIE_RST_L"},        # gpio497 
                    {"gpio": GPIO_BASE-15, "direction": "out", "value": 1, "desc": "IO_0.0 9539_TH_RST_L"}         # gpio496 
                ],
                "config_0": 0xc0, "config_1": 0x3f, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x03, "output_port_1": 0xc0
            },
            "9555_BEACON_LED": {
                "name": "pca9555_BEACON_LED", "address": 0x20, "parent": "9548_ROOT_GB", "channel": 6, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-16, "direction": "in"             , "desc": "IO_1.7 NONE"},     # gpio495  
                    {"gpio": GPIO_BASE-17, "direction": "out", "value": 1, "desc": "IO_1.6 7SEG_RG"},  # gpio494  
                    {"gpio": GPIO_BASE-18, "direction": "out", "value": 0, "desc": "IO_1.5 7SEG_RB"},  # gpio493  
                    {"gpio": GPIO_BASE-19, "direction": "out", "value": 0, "desc": "IO_1.4 7SEG_RD"},  # gpio492  
                    {"gpio": GPIO_BASE-20, "direction": "out", "value": 0, "desc": "IO_1.3 7SEG_RF"},  # gpio491  
                    {"gpio": GPIO_BASE-21, "direction": "out", "value": 0, "desc": "IO_1.2 7SEG_RC"},  # gpio490  
                    {"gpio": GPIO_BASE-22, "direction": "out", "value": 0, "desc": "IO_1.1 7SEG_RE"},  # gpio489  
                    {"gpio": GPIO_BASE-23, "direction": "out", "value": 0, "desc": "IO_1.0 7SEG_RA"},  # gpio488  
                    {"gpio": GPIO_BASE-24, "direction": "in"             , "desc": "IO_0.7 NONE"},     # gpio487  
                    {"gpio": GPIO_BASE-25, "direction": "out", "value": 0, "desc": "IO_0.6 7SEG_LA"},  # gpio486  
                    {"gpio": GPIO_BASE-26, "direction": "out", "value": 0, "desc": "IO_0.5 7SEG_LF"},  # gpio485  
                    {"gpio": GPIO_BASE-27, "direction": "out", "value": 1, "desc": "IO_0.4 7SEG_LG"},  # gpio484  
                    {"gpio": GPIO_BASE-28, "direction": "out", "value": 0, "desc": "IO_0.3 7SEG_LD"},  # gpio483  
                    {"gpio": GPIO_BASE-29, "direction": "out", "value": 0, "desc": "IO_0.2 7SEG_LE"},  # gpio482  
                    {"gpio": GPIO_BASE-30, "direction": "out", "value": 0, "desc": "IO_0.1 7SEG_LB"},  # gpio481  
                    {"gpio": GPIO_BASE-31, "direction": "out", "value": 0, "desc": "IO_0.0 7SEG_LC"}   # gpio480  
                ],
                "config_0": 0xff, "config_1": 0xff, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
            "9555_BOARD_ID": {
                "name": "pca9555_BOARD_ID", "address": 0x20, "parent": "9548_ROOT_GB", "channel": 2, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-32, "direction": "in", "desc": "IO_1.7 Board_ID_3"},    # gpio479 
                    {"gpio": GPIO_BASE-33, "direction": "in", "desc": "IO_1.6 Board_ID_2"},    # gpio478 
                    {"gpio": GPIO_BASE-34, "direction": "in", "desc": "IO_1.5 Board_ID_1"},    # gpio477 
                    {"gpio": GPIO_BASE-35, "direction": "in", "desc": "IO_1.4 Board_ID_0"},    # gpio476 
                    {"gpio": GPIO_BASE-36, "direction": "in", "desc": "IO_1.3 HW_REV_1"},      # gpio475 
                    {"gpio": GPIO_BASE-37, "direction": "in", "desc": "IO_1.2 HW_REV_0"},      # gpio474 
                    {"gpio": GPIO_BASE-38, "direction": "in", "desc": "IO_1.1 Build_REV_1"},   # gpio473 
                    {"gpio": GPIO_BASE-39, "direction": "in", "desc": "IO_1.0 Build_REV_0"},   # gpio472 
                    {"gpio": GPIO_BASE-40, "direction": "in", "desc": "IO_0.7 NONE"},          # gpio471 
                    {"gpio": GPIO_BASE-41, "direction": "in", "desc": "IO_0.6 NONE"},          # gpio470 
                    {"gpio": GPIO_BASE-42, "direction": "in", "desc": "IO_0.5 NONE"},          # gpio469 
                    {"gpio": GPIO_BASE-43, "direction": "in", "desc": "IO_0.4 NONE"},          # gpio468 
                    {"gpio": GPIO_BASE-44, "direction": "in", "desc": "IO_0.3 NONE"},          # gpio467 
                    {"gpio": GPIO_BASE-45, "direction": "in", "desc": "IO_0.2 NONE"},          # gpio466 
                    {"gpio": GPIO_BASE-46, "direction": "in", "desc": "IO_0.1 NONE"},          # gpio465 
                    {"gpio": GPIO_BASE-47, "direction": "in", "desc": "IO_0.0 NONE"}           # gpio464
                ],
                "config_0": 0xff, "config_1": 0xff, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
            "9539_VOL_MARGIN": {
                "name": "pca9539_VOL_MARGIN", "address": 0x76, "parent": "9548_ROOT_GB", "channel": 5, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-48, "direction": "in", "desc": "IO_1.7 P1V2_3_Low_Margin"},   # gpio463
                    {"gpio": GPIO_BASE-49, "direction": "in", "desc": "IO_1.6 P1V2_3_High_Margin"},  # gpio462
                    {"gpio": GPIO_BASE-50, "direction": "in", "desc": "IO_1.5 P0V9_Low_Margin"},     # gpio461 
                    {"gpio": GPIO_BASE-51, "direction": "in", "desc": "IO_1.4 P0V9_High_Margin"},    # gpio460 
                    {"gpio": GPIO_BASE-52, "direction": "in", "desc": "IO_1.3 P0V88_Low_Margin"},    # gpio459 
                    {"gpio": GPIO_BASE-53, "direction": "in", "desc": "IO_1.2 P0V88_High_Margin"},   # gpio458 
                    {"gpio": GPIO_BASE-54, "direction": "in", "desc": "IO_1.1 NI"},                  # gpio457 
                    {"gpio": GPIO_BASE-55, "direction": "in", "desc": "IO_1.0 NI"},                  # gpio456 
                    {"gpio": GPIO_BASE-56, "direction": "in", "desc": "IO_0.7 P2V5_Low_Margin"},     # gpio455 
                    {"gpio": GPIO_BASE-57, "direction": "in", "desc": "IO_0.6 P2V5_High_Margin"},    # gpio454 
                    {"gpio": GPIO_BASE-58, "direction": "in", "desc": "IO_0.5 P1V8_Low_Margin"},     # gpio453 
                    {"gpio": GPIO_BASE-59, "direction": "in", "desc": "IO_0.4 P1V8_High_Margin"},    # gpio452 
                    {"gpio": GPIO_BASE-60, "direction": "in", "desc": "IO_0.3 P1V2_1_Low_Margin"},   # gpio451 
                    {"gpio": GPIO_BASE-61, "direction": "in", "desc": "IO_0.2 P1V2_1_High_Margin"},  # gpio450 
                    {"gpio": GPIO_BASE-62, "direction": "in", "desc": "IO_0.1 P1V2_2_Low_Margin"},   # gpio449 
                    {"gpio": GPIO_BASE-63, "direction": "in", "desc": "IO_0.0 P1V2_2_High_Margin"}   # gpio448 
                ],
                "config_0": 0x0, "config_1": 0x03, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
            "9539_CPU_I2C": {
                "name": "pca9539_CPU_I2C", "address": 0x77, "parent": None, "channel": None, "pins": 16,
                "init_cfg": [
                    {"gpio": GPIO_BASE-64, "direction": "in", "desc": "IO_1.7"},   # gpio447 
                    {"gpio": GPIO_BASE-65, "direction": "in", "desc": "IO_1.6"},   # gpio446 
                    {"gpio": GPIO_BASE-66, "direction": "in", "desc": "IO_1.5"},   # gpio445 
                    {"gpio": GPIO_BASE-67, "direction": "in", "desc": "IO_1.4"},   # gpio444 
                    {"gpio": GPIO_BASE-68, "direction": "in", "desc": "IO_1.3"},   # gpio443 
                    {"gpio": GPIO_BASE-69, "direction": "in", "desc": "IO_1.2"},   # gpio442 
                    {"gpio": GPIO_BASE-70, "direction": "in", "desc": "IO_1.1"},   # gpio441 
                    {"gpio": GPIO_BASE-71, "direction": "in", "desc": "IO_1.0"},   # gpio440 
                    {"gpio": GPIO_BASE-72, "direction": "in", "desc": "IO_0.7"},   # gpio439 
                    {"gpio": GPIO_BASE-73, "direction": "in", "desc": "IO_0.6"},   # gpio438 
                    {"gpio": GPIO_BASE-74, "direction": "in", "desc": "IO_0.5"},   # gpio437 
                    {"gpio": GPIO_BASE-75, "direction": "in", "desc": "IO_0.4"},   # gpio436 
                    {"gpio": GPIO_BASE-76, "direction": "in", "desc": "IO_0.3"},   # gpio435 
                    {"gpio": GPIO_BASE-77, "direction": "in", "desc": "IO_0.2"},   # gpio434 
                    {"gpio": GPIO_BASE-78, "direction": "in", "desc": "IO_0.1"},   # gpio433 
                    {"gpio": GPIO_BASE-79, "direction": "in", "desc": "IO_0.0"}    # gpio432 
                ],
                "config_0": 0xff, "config_1": 0xff, "polarity_inv_0": 0x0, "polarity_inv_1": 0x0, "output_port_0": 0x0, "output_port_1": 0x0
            },
        }
        
        self.IOExpanders = self.APOLLO_IOExpanders
        self._update_gpio_base()
        self.board_id = self.brd_id_util.get_board_id()

        if self.board_id == BID.NCP1_1_PROTO:
            self.IOExpanders = self.APOLLO_IOExpanders
            self.ordered_ioexps = self.APOLLO_PROTO_IOExpanders_Order_List
        elif (self.board_id & BID.BUILD_REV_MASK) == BID.NCP1_1_ALPHA:
            self.IOExpanders = self.APOLLO_IOExpanders
            self.ordered_ioexps = self.APOLLO_ALPHA_IOExpanders_Order_List
        elif (self.board_id & BID.BUILD_REV_MASK) >= BID.NCP1_1_BETA:
            self.IOExpanders = self.APOLLO_BETA_IOExpanders
            self.ordered_ioexps = self.APOLLO_BETA_IOExpanders_Order_List
        else:
            self.logger.error("Board ID {0} invalid. Please check the Board ID IO Expander.".format(self.board_id))
            sys.exit(0)

    def _create_sysfs(self, path_parent, ioexp):
        try:
            sysfs_path = self.sysfs_util.get_sysfs_path(ioexp.bus_num, ioexp.address)
            if os.path.exists(sysfs_path):
                self.logger.info(ioexp.name + " is already exist")
                return

            with open(path_parent + "/" + self.sysfs_util.OP_NEW_DEV, 'w') as f:
                f.write(ioexp.NAME + " " + hex(ioexp.address))
            self.logger.info("Register " + ioexp.name + " in sysfs")
        except Exception as e:
            self.logger.error("Register IOExpander " + ioexp.name + " error: " + str(e))
            raise

    def _export_gpio(self, ioexp, pin, gpio_num):
        try:
            if (os.path.exists(self.sysfs_util.get_gpio_path(gpio_num))):
                self.logger.info(ioexp.name + "(pin:" + str(pin) + ") is already exist")
            else:
                with open(self.sysfs_util.get_gpio_root_path() + "/export", "w") as f:
                    f.write(str(gpio_num))
                    self.logger.info("Export " + ioexp.name + "(pin:" + str(pin) + ") at GPIO " + str(gpio_num))
        except Exception as e:
            self.logger.error("Export GPIO " + str(gpio_num) + " for " + ioexp.name + "(pin:" + str(pin) + ") error: " + str(e))
            raise

    def _unexport_gpio(self, ioexp, pin, gpio_num):
        try:
            if (os.path.exists(self.sysfs_util.get_gpio_path(gpio_num))):
                with open(self.sysfs_util.get_gpio_root_path() + "/unexport", "w") as f:
                    f.write(str(gpio_num))
                    self.logger.info("Unexport " + ioexp.name + "(pin:" + str(pin) + ") at GPIO " + str(gpio_num))
        except Exception as e:
            self.logger.error("Unexport GPIO for " + ioexp.name + "(pin:" + str(pin) + ") error: " + str(e))
            raise

    def _init_gpio(self, ioexp, pin, gpio_num):
        try:
            gpio_path = self.sysfs_util.get_gpio_path(gpio_num)
            gpio_dir_path = gpio_path + "/direction"            
            direction = ioexp.init_cfg[pin]["direction"]
            
            if (os.path.exists(gpio_path)):
                # Set direction
                with open(gpio_dir_path, "w") as f:
                    if direction == "out":
                        # If no "value" in dict, means this pin is for input, config next one
                        key = "value"
                        if key not in ioexp.init_cfg[pin]:
                            return

                        # This pin is for output, set initial value
                        value = ioexp.init_cfg[pin]["value"]
                        
                        # set output direction and init value with high/low 
                        if value == 0:
                            direction = "low"
                        else:
                            direction = "high"
                    
                    f.write(direction)                    
                        
                self.logger.info("Set " + ioexp.name + "(pin:" + str(pin) + ") direction: " + direction)                
            else:
                self.logger.warning(ioexp.name + "(pin:" + str(pin) + ") is not exported yet")
        except Exception as e:
            self.logger.error("Initialize " + ioexp.name + "(pin:" + str(pin) + ") fail, error: " + str(e))
            raise

    def _remove_sysfs(self, path_parent, dev_info):
        try:
            with open(path_parent + "/" + self.sysfs_util.OP_DEL_DEV, 'w') as f:
                f.write(hex(dev_info["address"]))
                self.logger.info("Un-register " + dev_info["name"])
        except Exception:
            raise

    def _write_gpio(self, sysfs_path, value):
        try:
            if isinstance(value, int):
                value = str(value)
                                    
            if os.path.exists(sysfs_path):
                with open(sysfs_path, "w") as f:
                    f.write(value)
            else:
                raise IOError("sysfs_path does not exist: {0}".format(sysfs_path))
                return 0            
        except Exception as e:            
            self.logger.error(e)
            raise

    def _read_gpio(self, sysfs_path):
        try:
            if os.path.exists(sysfs_path):
                with open(sysfs_path, "r") as f:
                    content = f.read()
                if content != None:
                    return content
            else:
                raise IOError("sysfs_path does not exist: {0}".format(sysfs_path))
                return 0            
        except Exception as e:
            self.logger.error(e)
            raise
    
    def _update_gpio_base(self):        
        gpiochip_max = 0
        retry_max = 10
        
        try:
            #get gpiochip max        
            output = subprocess.getoutput("ls /sys/class/gpio/ | sort -r | grep -m1 gpiochip")                                                    
            if output == "":
                subprocess.getoutput("echo 'pca9539 0x74' > " + self.sysfs_util.get_new_dev_path(0))
                
                for _ in range(retry_max):                
                    output = subprocess.getoutput("ls /sys/class/gpio/ | sort -r | grep -m1 gpiochip")
                    if output != "":                        
                        break
                    time.sleep(0.2)
                
                subprocess.getoutput("echo '0x74' > " + self.sysfs_util.get_del_dev_path(0))
            
            #get max 
            if output != "":
                gpiochip_max = int(output.replace("gpiochip", ""))        
                                    
            # gpiochip_max <= 255
            if 0 < gpiochip_max <= 255:                
                #update IOExpanders gpioN = gpioN - 256
                for ioexp_name in self.APOLLO_ALPHA_IOExpanders_Order_List:
                    for gpio_config in self.APOLLO_IOExpanders[ioexp_name]["init_cfg"]:
                        gpio_config["gpio"] = gpio_config["gpio"] - 256
                for ioexp_name in self.APOLLO_BETA_IOExpanders_Order_List:
                    for gpio_config in self.APOLLO_BETA_IOExpanders[ioexp_name]["init_cfg"]:
                        gpio_config["gpio"] = gpio_config["gpio"] - 256
                
        except Exception as e:
            self.logger.error(e)
            raise

    def init(self, i2c_mux):
        # Create sysfs, export gpio and initial gpio
        for ioexp_name in self.ordered_ioexps:
            try:
                if self.IOExpanders[ioexp_name]["parent"] is None:
                    bus_num = 0
                else:
                    bus_num = i2c_mux[self.IOExpanders[ioexp_name]["parent"]].chnl_bus[self.IOExpanders[ioexp_name]["channel"]]
                if ioexp_name == "9539_HOST_GPIO_I2C":
                    ioexp = PCA9539(self.IOExpanders[ioexp_name], bus_num)
                else:
                    ioexp = PCA9535(self.IOExpanders[ioexp_name], bus_num)
                
                #check IOExpander exists
                retcode, _ = subprocess.getstatusoutput("i2cget -f -y {} {} 0x0".format(bus_num, ioexp.address))
                if retcode != 0:                
                    self.logger.error("IOExpander {} (0x{:02X}) does not exists on bus {}".format(ioexp.name,
                                                                                            ioexp.address,
                                                                                            bus_num))
                    sys.exit()

                #create sysfs
                self.logger.info("Create sysfs for " + ioexp.name)
                path_parent = self.sysfs_util.get_bus_path(ioexp.bus_num)
                self._create_sysfs(path_parent, ioexp)
                
                #export gpio
                for i in range(ioexp.pins):
                    self._export_gpio(ioexp, i, ioexp.init_cfg[i]["gpio"])
                    self._init_gpio(ioexp, i, ioexp.init_cfg[i]["gpio"])

            except Exception:
                raise

    def deinit(self, i2c_mux):
        for ioexp_name in self.ordered_ioexps:
            try:
                if self.IOExpanders[ioexp_name]["parent"] is None:
                    bus_num = 0
                else:
                    bus_num = i2c_mux[self.IOExpanders[ioexp_name]["parent"]].chnl_bus[self.IOExpanders[ioexp_name]["channel"]]

                if ioexp_name == "9539_HOST_GPIO_I2C":
                    ioexp = PCA9539(self.IOExpanders[ioexp_name], bus_num)
                else:
                    ioexp = PCA9535(self.IOExpanders[ioexp_name], bus_num)

                path_parent = self.sysfs_util.get_bus_path(bus_num)

                for i in range(ioexp.pins):
                    self._unexport_gpio(ioexp, i, ioexp.init_cfg[i]["gpio"])

                sysfs_path = self.sysfs_util.get_sysfs_path(bus_num, self.IOExpanders[ioexp_name]["address"])
                if os.path.exists(sysfs_path):
                    self._remove_sysfs(path_parent, self.IOExpanders[ioexp_name])
            except Exception:
                raise

    def set_uart_mux(self, value):
        try:
            gpio_num = self.IOExpanders["9539_HOST_GPIO_I2C"]["init_cfg"][10]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_uart_mux {0} failed, error: {1}".format(value, e))
            raise              
            
    def set_usb_mux(self, value):
        try:
            gpio_num = self.IOExpanders["9539_HOST_GPIO_I2C"]["init_cfg"][11]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_usb_mux {0} failed, error: {1}".format(value, e))
            raise 
    
    def set_sys_led_g(self, value):
        try:
            gpio_num = self.IOExpanders["9539_SYS_LED"]["init_cfg"][15]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self.logger.debug("set_sys_led_g(), _write_gpio({0}, {1})".format(sysfs_path, value))
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_sys_led_g {0} failed, error: {1}".format(value, e))
            raise 
            
    def set_fan_led_en(self, value):
        try:
            gpio_num = self.IOExpanders["9539_SYS_LED"]["init_cfg"][14]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self.logger.debug("set_fan_led_en(), _write_gpio({0}, {1})".format(sysfs_path, value))
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_fan_led_en {0} failed, error: {1}".format(value, e))
            raise
     
    def set_fan_led_y(self, value):
        try:
            gpio_num = self.IOExpanders["9539_SYS_LED"]["init_cfg"][13]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_fan_led_y {0} failed, error: {1}".format(value, e))
            raise 
    
    def set_psu0_led_y(self, value):
        try:
            gpio_num = self.IOExpanders["9539_SYS_LED"]["init_cfg"][12]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self.logger.debug("set_psu0_led_y(), _write_gpio({0}, {1})".format(sysfs_path, value))
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_psu0_led_y {0} failed, error: {1}".format(value, e))
            raise 
     
    def set_psu1_led_y(self, value):
        try:
            gpio_num = self.IOExpanders["9539_SYS_LED"]["init_cfg"][11]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self.logger.debug("set_psu1_led_y(), _write_gpio({0}, {1})".format(sysfs_path, value))
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_psu1_led_y {0} failed, error: {1}".format(value, e))
            raise
        
    def set_psu0_pwrok(self, value):
        try:
            gpio_num = self.IOExpanders["9539_SYS_LED"]["init_cfg"][7]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self.logger.debug("set_psu0_pwrok(), _write_gpio({0}, {1})".format(sysfs_path, value))
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_psu0_pwrok {0} failed, error: {1}".format(value, e))
            raise 
     
    def set_psu1_pwrok(self, value):
        try:
            gpio_num = self.IOExpanders["9539_SYS_LED"]["init_cfg"][6]["gpio"]
            sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
            self.logger.debug("set_psu1_pwrok(), _write_gpio({0}, {1})".format(sysfs_path, value))
            self._write_gpio(sysfs_path, value)            
        except Exception as e:
            self.logger.error("set_psu1_pwrok {0} failed, error: {1}".format(value, e))
            raise
        
    def set_beacon_led(self, seg7_left, seg7_right):
        try:
            #left beacon LED, IO_0.0~IO_0.6
            j=0
            for i in range(15, 8, -1):            
                gpio_num = self.IOExpanders["9555_BEACON_LED"]["init_cfg"][i]["gpio"]            
                sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
                value = seg7_left[j]
                self.logger.debug("set_beacon_led(), _write_gpio({}, {})".format(sysfs_path, value))
                self._write_gpio(sysfs_path, value)
                j+=1
            
            #right beacon LED, IO_1.0~IO_1.6
            j=0
            for i in range(7, 0, -1):            
                gpio_num = self.IOExpanders["9555_BEACON_LED"]["init_cfg"][i]["gpio"]            
                sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
        
                value = seg7_right[j]
                self.logger.debug("set_beacon_led(), _write_gpio({}, {})".format(sysfs_path, value))
                self._write_gpio(sysfs_path, value)   
                j+=1                      
        except Exception as e:
            self.logger.error("set_beacon_led {0} failed, error: {1}".format(value, e))
            raise                              

    def get_cpld_to_cpu_intr(self):
        gpio_vals = []
        try:
            for i in range(2, 8):
                gpio_num = self.IOExpanders["9539_HOST_GPIO_I2C"]["init_cfg"][i]["gpio"]
                sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)        
                gpio_vals.append(int(self._read_gpio(sysfs_path)))
            return gpio_vals              
        except Exception as e:
            self.logger.error("get_cpld_to_cpu_intr() failed, error: {}".format(e))
            raise
    
    def dump_reg(self, ioexp_name):
        reg_vals = []
        
        try:
            gpios = self.IOExpanders[ioexp_name]["init_cfg"]
            
            for gpio in gpios:
                gpio_num = gpio["gpio"]
                sysfs_path = self.sysfs_util.get_gpio_val_path(gpio_num)
                gpio_content = self._read_gpio(sysfs_path)
                gpio_value = int(gpio_content)
                reg_vals.append(gpio_value)
            
            return reg_vals
        except Exception as e:
            self.logger.error("dump_reg() failed, error: {}".format(e))
            raise

    def dump_sysfs(self):
        ret = {}

        try:
            for ioexp_name in self.ordered_ioexps:
                gpios = self.IOExpanders[ioexp_name]["init_cfg"]
                ret[ioexp_name] = {}

                for gpio in gpios:
                    gpio_num = gpio["gpio"]
                    gpio_desc = gpio["desc"]
                    sysfs_path = self.sysfs_util.get_gpio_path(gpio_num)
                    
                    ret[ioexp_name][gpio_num] = {"desc": gpio_desc, "sysfs": sysfs_path}
            return ret

        except Exception as e:
            self.logger.error("dump_sysfs() failed, error: {}".format(e))
            raise

