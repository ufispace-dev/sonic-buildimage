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

import sys
import json
from time import sleep
from itertools import chain

from bsp.utility.cpld_utility import CPLDUtility
from bsp.utility.eeprom_utility import EEPRomUtility
from bsp.utility.ipmi_utility import IPMIUtility
from bsp.utility.led_utility import LEDUtility
from bsp.utility.psu_utility import PSUUtility
from bsp.utility.qsfp_utility import QSFPUtility
from bsp.utility.qsfpdd_utility import QSFPDDUtility
from bsp.utility.sfp_utility import SFPUtility
from bsp.utility.uartmux_utility import UARTMuxUtility
from bsp.utility.usbmux_utility import USBMuxUtility
from bsp.utility.thermal_utility import ThermalUtility
from bsp.utility.bsp_utility import BSPUtility
from bsp.utility.rov_utility import ROVUtility
from bsp.utility.intr_utility import INTRUtility
from bsp.const.const import QSFP
from bsp.const.const import QSFPDD
from bsp.const.const import CPLDConst
from bsp.const.const import Led
from bsp.gpio.ioexp import IOExpander

def _group_to_range(group):
    group = ''.join(group.split())
    sign, g = ('-', group[1:]) if group.startswith('-') else ('', group)
    r = g.split('-', 1)
    r[0] = sign + r[0]
    r = sorted(int(__) for __ in r)
    return range(r[0], 1 + r[-1])

def _rangeexpand(txt):
    ranges = chain.from_iterable(_group_to_range(__) for __ in txt.split(','))
    return sorted(set(ranges))
    
def cpld_usage(cmd):
    cpld_max = CPLDConst.CPLD_MAX - 1
    print("Usage: " + cmd + " CPLD 1|2|3|4|5|help [option1]")
    print("    1: Get board ID")
    print("    2: Get MB CPLD ID")
    print("    3: Get CPLD version")
    print("       option1: 0 for CPU, 1 for MB")
    print("    4: Get CPLD port interrupt status")
    print("       option1: CPLD number, 0-{0}".format(cpld_max))
    print("    5: Reset device")
    print("       option1: 0 for J2, 1 for Gearbox, 2 for Retimer, 6 for OP2_CRST, 7 for OP2_PERST, 8 for OP2_SRST")
    print("    6: Get Reset control")
    print("       option1: 0 for J2, 6 for OP2_CRST, 7 for OP2_PERST, 8 for OP2_SRST")
    print("    7: Set Reset control")
    print("       option1: 0 for J2, 6 for OP2_CRST, 7 for OP2_PERST, 8 for OP2_SRST")
    print("       option2: 0 for RESET, 1 for NO_RESET")
    
def ut_cpld(argv):
    try:
        util = CPLDUtility()

        if len(argv) < 3:
            cpld_usage(argv[0])
        elif argv[2] == '1':
            print(json.dumps(util.get_board_info(), sort_keys=False, indent=4))
        elif argv[2] == '2':
            print(json.dumps(util.get_cpld_id(), sort_keys=False, indent=4))
        elif argv[2] == '3':
            if len(argv) < 4:
                cpld_usage(argv[0])
            else:
                print(json.dumps(util.get_cpld_version(int(argv[3])), sort_keys=False, indent=4))
        elif argv[2] == '4':       
            if len(argv) < 4:
                cpld_usage(argv[0])
            else:      
                cpld_list = _rangeexpand(argv[3])
                for cpld in cpld_list:
                    print("[" + str(cpld) + "] " + str(util.get_cpld_port_interrupt(cpld)))
        elif argv[2] == '5':       
            if len(argv) < 4:
                cpld_usage(argv[0])
            else:      
                util.reset_dev(int(argv[3]))                    
        elif argv[2] == '6':
            if len(argv) < 4:
                cpld_usage(argv[0])
            else:
                dev_list = _rangeexpand(argv[3])
                for dev in dev_list:
                    print("[" + str(dev) + "] " + json.dumps(util.get_reset_ctrl(int(dev)), sort_keys=False, indent=4))                  
        elif argv[2] == '7':
            if len(argv) < 5:
                cpld_usage(argv[0])
            else:
                util.set_reset_ctrl(int(argv[3]), int(argv[4]))                
        else:
            cpld_usage(argv[0])
    except:
        raise

def eeprom_usage(cmd):
    qsfpdd_max_port = QSFPDD.MAX_PORT - 1
    ports = QSFP.MAX_PORT - 1
    
    print("Usage: " + cmd + " EEPROM 1|2|3|help [option1]")
    print("    1: Dump EEPROM content from CPU")
    print("    2: Dump EEPROM content from specific QSFP port")
    print("       option1: Port number, 0-{0}".format(ports))
    print("    3: Dump EEPROM content from specific QSFPDD port")
    print("       option1: Port number, 0-{0}".format(qsfpdd_max_port))
    print("    4: Get EEPROM info from specific QSFP port")
    print("       option1: Port number, 0-{0}".format(ports))
    print("    5: Get EEPROM info from specific QSFPDD port")
    print("       option1: Port number, 0-{0}".format(qsfpdd_max_port))
    print("    6: Get EEPROM i2c bus num from specific QSFP port")
    print("       option1: Port number, 0-{0}".format(ports))
    print("    7: Get EEPROM i2c bus num from specific QSFPDD port")
    print("       option1: Port number, 0-{0}".format(qsfpdd_max_port))

def ut_eeprom(argv):
    try:
        util = EEPRomUtility()

        if len(argv) < 3:
            eeprom_usage(argv[0])
        elif argv[2] != '1' and len(argv) < 4:
            eeprom_usage(argv[0])
        elif argv[2] == '1':
            print(util.dump_cpu_eeprom())
        elif argv[2] == '2':
            port_list = _rangeexpand(argv[3])
            for port in port_list:
                print(util.dump_qsfp_eeprom(port))
        elif argv[2] == '3':            
            port_list = _rangeexpand(argv[3])
            for port in port_list:
                print(util.dump_qsfpdd_eeprom(port))
        elif argv[2] == '4':
            port_list = _rangeexpand(argv[3])
            for port in port_list:
                print(json.dumps(util.get_qsfp_info(port), sort_keys=False, indent=4))
        elif argv[2] == '5':
            port_list = _rangeexpand(argv[3])
            for port in port_list:
                print(json.dumps(util.get_qsfpdd_info(port), sort_keys=False, indent=4))
        elif argv[2] == '6':
            port_list = _rangeexpand(argv[3])
            for port in port_list:
                print(util.get_qsfp_bus_num(port))
        elif argv[2] == '7':
            port_list = _rangeexpand(argv[3])
            for port in port_list:
                print(util.get_qsfpdd_bus_num(port))
        else:
            eeprom_usage(argv[0])
    except:
        raise

def ipmi_usage(cmd):
    print("Usage: " + cmd + " IPMI 1|2|help")
    print("    1: Get Sensor Info")
    print("    2: Check IPMI Dev")

def ut_ipmi(argv):
    try:
        util = IPMIUtility()

        if len(argv) < 3:
            ipmi_usage(argv[0])
        elif argv[2] == '1':
            sensors = util.get_sensor()
            for i in range(len(sensors)):
                print("{:20}| {:10}| {:10}| {:5}".format(sensors[i].name, sensors[i].value, sensors[i].unit, sensors[i].status))
        elif argv[2] == '2':
            print(util.get_ipmidev_status())    
        else:
            ipmi_usage(argv[0])
    except:
        raise

def led_usage(cmd):
    max_port = QSFPDD.MAX_PORT - 1    
    max_beacon = Led.BEACON_MAX
    print("Usage: " + cmd + " LED 1|2|3|4|5|help [option1] [option2]")
    print("    1: Set System LED")
    print("       option1: 0 for System, 1 for Fan, 2 for PSU0, 3 for PSU1")
    print("       option2: 0 for OFF, 1 for Yellow, 2 for Green")    
    print("    2: Set QSFPDD LED")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("       option2: 0 for OFF, 1 for Red, 2 for Green, 3 for Blue")    
    print("       option3: 0 for solid, 1 for blinking")
    print("    3: Set Beacon Number")
    print("       option1: Beacon number, 0-{0}".format(max_beacon))
    print("    4: Auto Test")    
    print("       option1: 0 for System LED, 1 for QSFPDD LED, 2 for Beacon LED")    
    print("    5: Get System LED")
    print("       option1: 0 for Fan, 1 for System, 2 for PSU0, 3 for PSU1")    

def ut_led(argv):
    try:
        util = LEDUtility()

        if len(argv) < 4:
            led_usage(argv[0])
        elif argv[2] == '1' and len(argv) == 5:
            util.set_sys_led(int(argv[3]), int(argv[4]))        
        elif argv[2] == '2' and len(argv) == 6:
            port_list = _rangeexpand(argv[3])
            for port in port_list:
                util.set_qsfpdd_led(port, int(argv[4]), int(argv[5]))
        elif argv[2] == '3' and len(argv) == 4:
            util.set_beacon_led_num(int(argv[3])) 
        elif argv[2] == '4' and len(argv) == 4:
            if argv[3] == '0':
                util.ut_sysled()
            elif argv[3] == '1':
                util.ut_qsfpdd_led()
            elif argv[3] == '2':
                util.ut_beacon_led()    
            else:
                led_usage(argv[0])                               
        elif argv[2] == '5' and len(argv) == 4:
            led_list = _rangeexpand(argv[3])
            for led in led_list:                
                print("[" + str(led) + "] " + json.dumps(util.get_sys_led(int(led)), sort_keys=False, indent=4))        
        else:
            led_usage(argv[0])
    except:
        raise

def psu_usage(cmd):
    print("Usage: " + cmd + " PSU 1|2|help [option1]" )
    print("    1: Get PSU Presence")
    print("       option1: 0 for PSU0, 1 for PSU1")
    print("    2: Get PSU Power Status")
    print("       option1: 0 for PSU0, 1 for PSU1")

def ut_psu(argv):
    try:
        util = PSUUtility()

        if len(argv) < 4:
            psu_usage(argv[0])
            return
        
        psu_list = _rangeexpand(argv[3])
        for psu in psu_list:
            if argv[2] == '1':                
                print("[{}] {}".format(psu, util.get_psu_presence(psu)))
            elif argv[2] == '2':
                print("[{}] {}".format(psu, util.get_psu_power_ok(psu)))
            else:
                psu_usage(argv[0])
    except:
        raise

def qsfp_usage(cmd):
    max_port = QSFP.MAX_PORT - 1  
    print("Usage: " + cmd + " QSFP 1|2|3|4|5|6|7|8|9|help [option1] [option2]")
    print("    1: Get QSFP port presence")
    print("       option1: Port number, 0-{0}".format(max_port))    
    print("    2: Get Low Power Mode setting of QSFP port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("    3: Set Low Power Mode to QSFP port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("       option2: 0 for disable, 1 for enable")
    print("    4: Auto-test Power Mode setting of QSFP port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("       option2: 0 for disable, 1 for enable")    
    print("    5: Reset QSFP port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("    6: Set QSFP reset status")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("       option2: reset status, 0 for reset, 1 for no reset")
    print("    7: Get QSFP reset status")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("    8: Auto-test reset status of QSFP port")
    print("       option1: Port number, 0-{0}".format(max_port))    
    print("       option2: reset status, 0 for reset, 1 for no reset")
    print("    9: Get QSFP port interrupt status")
    print("       option1: Port number, 0-{0}".format(max_port))
    
def ut_qsfp(argv):
    try:
        util = QSFPUtility()

        if len(argv) < 4:
            qsfp_usage(argv[0])
            return
        
        port_list = _rangeexpand(argv[3])
        
        for port in port_list:
            if argv[2] == '1':
                print("[{}] {}".format(port, util.get_presence(port)))            
            elif argv[2] == '2':                
                print("[{}] {}".format(port, util.get_lp_mode(port)))
            elif argv[2] == '3':
                if len(argv) < 5:
                    qsfp_usage(argv[0])
                else:
                    util.set_lp_mode(port, int(argv[4]))    
            elif argv[2] == '4':
                if len(argv) < 5:
                    qsfp_usage(argv[0])
                else:
                    print("[{}] {}".format(port, util.get_lp_mode(port)), end='', flush=True)
                    util.set_lp_mode(port, int(argv[4]))
                    print(" -> {}".format(util.get_lp_mode(port)["lp_mode"]))
            elif argv[2] == '5':
                util.reset_port(port)
            elif argv[2] == '6':
                if len(argv) < 5:
                    qsfp_usage(argv[0])
                else:
                    util.set_reset(port, int(argv[4]))
            elif argv[2] == '7':                
                print("[{}] {}".format(port, util.get_reset(port)))
            elif argv[2] == '8':
                if len(argv) < 5:
                    qsfp_usage(argv[0])
                else:                    
                    print("[{}] {}".format(port, util.get_reset(port)), end='', flush=True)
                    util.set_reset(port, int(argv[4]))
                    print(" -> {}".format(util.get_reset(port)["reset"]))
            elif argv[2] == '9':
                print("[{}] {}".format(port, util.get_interrupt(port)))
            else:
                qsfp_usage(argv[0])
                
    except:
        raise

def qsfpdd_usage(cmd):
    max_port = QSFPDD.MAX_PORT - 1
    print("Usage: " + cmd + " QSFPDD 1|2|3|4|5|6|7|8|9|help [option1] [option2]")
    print("    1: Get QSFPDD port presence")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("    2: Get Low Power Mode setting of QSFPDD port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("    3: Set Low Power Mode to QSFPDD port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("       option2: 0 for disable, 1 for enable")    
    print("    4: Auto-test Power Mode setting of QSFPDD port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("       option2: 0 for disable, 1 for enable")    
    print("    5: Reset QSFPDD port")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("    6: Set QSFPDD reset status")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("       option2: reset status, 0 for reset, 1 for no reset")
    print("    7: Get QSFPDD reset status")
    print("       option1: Port number, 0-{0}".format(max_port))
    print("    8: Auto-test reset status of QSFPDD port")
    print("       option1: Port number, 0-{0}".format(max_port))    
    print("       option2: reset status, 0 for reset, 1 for no reset")
    print("    9: Get QSFPDD port interrupt status")
    print("       option1: Port number, 0-{0}".format(max_port))
    
def ut_qsfpdd(argv):
    try:
        util = QSFPDDUtility()

        if len(argv) < 4:
            qsfpdd_usage(argv[0])
            return
        
        port_list = _rangeexpand(argv[3])
        for port in port_list:
            if argv[2] == '1':
                print("[{}] {}".format(port, util.get_presence(port)))
            elif argv[2] == '2':                
                print("[{}] {}".format(port, util.get_lp_mode(port)))
            elif argv[2] == '3':
                if len(argv) < 5:
                    qsfpdd_usage(argv[0])
                else:
                    util.set_lp_mode(port, int(argv[4]))            
            elif argv[2] == '4':
                if len(argv) < 5:
                    qsfpdd_usage(argv[0])
                else:
                    print("[{}] {}".format(port, util.get_lp_mode(port)), end='', flush=True)
                    util.set_lp_mode(port, int(argv[4]))
                    print(" -> {}".format(util.get_lp_mode(port)["lp_mode"]))
            elif argv[2] == '5':
                util.reset_port(port)
            elif argv[2] == '6':
                if len(argv) < 5:
                    qsfpdd_usage(argv[0])
                else:
                    util.set_reset(port, int(argv[4]))
            elif argv[2] == '7':
                print(util.get_reset(port))
            elif argv[2] == '8':
                if len(argv) < 5:
                    qsfpdd_usage(argv[0])
                else:
                    print("[{}] {}".format(port, util.get_reset(port)), end='', flush=True)
                    util.set_reset(port, int(argv[4]))
                    print(" -> {}".format(util.get_reset(port)["reset"]))
            elif argv[2] == '9':
                print("[{}] {}".format(port, util.get_interrupt(port)))
            else:
                qsfpdd_usage(argv[0])
    except:
        raise

def sfp_usage(cmd):
    print("Usage: " + cmd + " SFP 1|2|3|4|5|help [option1] [option2]")
    print("    1: Get SFP+ port presence")
    print("       option1: Port number, 0-1")
    print("    2: Get SFP+ port RX Lost")
    print("       option1: Port number, 0-1")
    print("    3: Get SFP+ port TX Fault")
    print("       option1: Port number, 0-1")
    print("    4: Get SFP+ Tx disable")
    print("       option1: Port number, 0-1")
    print("    5: Set SFP+ Tx disable")
    print("       option1: Port number, 0-1")
    print("       option2: 0 for enable, 1 for disable")
    
def ut_sfp(argv):
    try:
        util = SFPUtility()

        if len(argv) < 4:
            sfp_usage(argv[0])
            return
        
        port_list = _rangeexpand(argv[3])
        for port in port_list:
            if argv[2] == '1':
                print(util.get_presence(port))
            elif argv[2] == '2':
                print(util.get_rx_los(port))
            elif argv[2] == '3':
                print(util.get_tx_fault(port))
            elif argv[2] == '4':
                print(util.get_tx_disable(port))
            elif argv[2] == '5':
                if len(argv) < 5:
                    sfp_usage(argv[0])
                else:
                    util.set_tx_disable(port, int(argv[4]))            
            else:
                sfp_usage(argv[0])
    except:
        raise

def uart_mux_usage(cmd):
    print("Usage: " + cmd + " UARTMux 1|2|help [option1]" )
    print("    1: Set UART Mux (Warning: Don't run this command under console, use SSH instead)")
    print("       option1: 0 for CPU, 1 for BMC")
    print("    2: Set UART Mux (CPU(5s) -> BMC(5s) -> CPU)")    

def ut_uart_mux(argv):
    try:
        util = UARTMuxUtility()

        if len(argv) < 3:
            uart_mux_usage(argv[0])
        elif argv[2] == '1' and len(argv) == 4:
            util.set_uart_mux(int(argv[3]))
        elif argv[2] == '2':
            util.set_uart_mux(0)
            sleep(5)
            util.set_uart_mux(1)
            sleep(5)
            util.set_uart_mux(0)
        else:
            uart_mux_usage(argv[0])
    except:
        raise

def usb_mux_usage(cmd):
    print("Usage: " + cmd + " USBMux 1|help [option1]" )
    print("    1: Set USB Mux")
    print("       option1: 0 for CPU, 1 for BMC")

def ut_usb_mux(argv):
    try:
        util = USBMuxUtility()

        if len(argv) < 4:
            usb_mux_usage(argv[0])
        elif argv[2] == '1':
            util.set_usb_mux(int(argv[3]))
        else:
            usb_mux_usage(argv[0])
    except:
        raise

def thermal_usage(cmd):
    print("Usage: " + cmd + " Thermal 1|2|help" )
    print("    1: Show CPU Core temp")
    print("    2: Show TMP75 on CPU board")

def ut_thermal(argv):
    try:
        util = ThermalUtility()

        if len(argv) < 3:
            thermal_usage(argv[0])
        elif argv[2] == '1':
            print(util.get_cpu_core_temp())
        elif argv[2] == '2':
            print(util.get_cpu_board_tmp75())
        else:
            thermal_usage(argv[0])
    except:
        raise
    
def bsp_usage(cmd):
    print("Usage: " + cmd + " BSP 1|help" )
    print("    1: Show BSP version")    
    print("    2: Show BSP Init Status")
def ut_bsp(argv):
    try:
        util = BSPUtility()

        if len(argv) < 3:
            bsp_usage(argv[0])
        elif argv[2] == '1':
            print(util.get_version())        
        elif argv[2] == '2':
            print(util.is_bsp_inited())        
        else:
            bsp_usage(argv[0])
    except:
        raise    
 
def rov_usage(cmd):
    print("Usage: " + cmd + " ROV 1|2|help" )
    print("    1: Get J2 ROV info")    
    print("    2: Set J2 ROV")

def ut_rov(argv):
    try:
        util = ROVUtility()

        if len(argv) < 3:
            rov_usage(argv[0])
        elif argv[2] == '1':
            print(json.dumps(util.get_j2_rov(), sort_keys=False, indent=4))
        elif argv[2] == '2':
            util.set_j2_rov()            
        else:
            rov_usage(argv[0])
    except:
        raise

def intr_usage(cmd):
    cpld_max = CPLDConst.CPLD_MAX - 1
    print("Usage: " + cmd + " INTR 1|2|3|4|5|6|7|8|9|10|11|help [option1]")
    print("    1: Init I2C Alert")
    print("    2: Clear I2C Alert")
    print("    3: Clear All Intr")
    print("    4: Get CPLD to CPU Interrupt")
    print("    5: Get All CPLD Interrupt")
    print("    6: Get CPLD Interrupt")
    print("       option1: CPLD number, 0-{0}".format(cpld_max))
    print("    7: Get Gearbox Interrupt")
    print("    8: Get Retimer Interrupt")
    print("    9: Deinit I2C Alert")
    print("    10: Get Alert GPIO")
    print("    11: Get Alert DIS")

def ut_intr(argv):
    try:
        util = INTRUtility()

        if len(argv) < 3:
            intr_usage(argv[0])
        elif argv[2] == '1':
            util.init_i2c_alert()
        elif argv[2] == '2':
            util.clear_i2c_alert()
        elif argv[2] == '3':
            util.clear_all_intr()
        elif argv[2] == '4':
            print(json.dumps(util.get_cpld_to_cpu_intr(), sort_keys=False, indent=4))
        elif argv[2] == '5':
            print(json.dumps(util.get_all_cpld_intr(), sort_keys=False, indent=4))
        elif argv[2] == '6':
            if len(argv) < 4:
                intr_usage(argv[0])
            else:      
                cpld_list = _rangeexpand(argv[3])
                for cpld in cpld_list:
                    print("[" + str(cpld) + "] " + str(util.get_cpld_intr(cpld)))
        elif argv[2] == '7':
            print(json.dumps(util.get_gbox_intr(), sort_keys=False, indent=4))
        elif argv[2] == '8':
            print(json.dumps(util.get_retimer_intr(), sort_keys=False, indent=4))    
        elif argv[2] == '9':
            util.deinit_i2c_alert()
        elif argv[2] == '10':
            print(util.get_alert_gpio())
        elif argv[2] == '11':
            print(util.get_alert_dis())
        else:
            intr_usage(argv[0])
    except:
        raise
        
def sysfs_usage(cmd):
    print("Usage: " + cmd + " SYSFS 1|2|help [option1]")
    print("    1: Dump GPIO sysfs")
    print("    2: Dump EEPROM sysfs")    

def ut_sysfs(argv):
    try:
        ioexp_util = IOExpander()
        eeprom_util = EEPRomUtility()

        if len(argv) < 3:
            sysfs_usage(argv[0])
        elif argv[2] == '1':
            print(json.dumps(ioexp_util.dump_sysfs(), sort_keys=False, indent=4))
        elif argv[2] == '2':
            print(json.dumps(eeprom_util.dump_sysfs(), sort_keys=False, indent=4))                
        else:
            sysfs_usage(argv[0])
    except:
        raise

def main():
    if len(sys.argv) < 2:
        print("\nUsage: " + sys.argv[0] + " CPLD|EEPROM|IPMI|LED|PSU|QSFP|QSFPDD|SFP|UARTMux|USBMux|Thermal|BSP|ROV|INTR|SYSFS|help")
        return

    if sys.argv[1] == 'CPLD':
        ut_cpld(sys.argv)
    elif sys.argv[1] == 'EEPROM':
        ut_eeprom(sys.argv)
    elif sys.argv[1] == 'IPMI':
        ut_ipmi(sys.argv)
    elif sys.argv[1] == 'LED':
        ut_led(sys.argv)
    elif sys.argv[1] == 'PSU':
        ut_psu(sys.argv)
    elif sys.argv[1] == 'QSFP':
        ut_qsfp(sys.argv)
    elif sys.argv[1] == 'QSFPDD':
        ut_qsfpdd(sys.argv)
    elif sys.argv[1] == 'SFP':
        ut_sfp(sys.argv)
    elif sys.argv[1] == 'UARTMux':
        ut_uart_mux(sys.argv)
    elif sys.argv[1] == 'USBMux':
        ut_usb_mux(sys.argv)
    elif sys.argv[1] == 'Thermal':
        ut_thermal(sys.argv)
    elif sys.argv[1] == 'BSP':
        ut_bsp(sys.argv)    
    elif sys.argv[1] == 'ROV':
        ut_rov(sys.argv)    
    elif sys.argv[1] == 'INTR':
        ut_intr(sys.argv)
    elif sys.argv[1] == 'SYSFS':
        ut_sysfs(sys.argv)   
    elif sys.argv[1] == 'help':
        print("\nUsage: " + sys.argv[0] + " CPLD|EEPROM|IPMI|LED|PSU|QSFP|QSFPDD|SFP|UARTMux|USBMux|Thermal|BSP|ROV|INTR|SYSFS|help")
    else:
        print("Invalid arguments:")

        # print command line arguments
        for arg in sys.argv[1:]:
            print(arg)
        print("\nUsage: " + sys.argv[0] + " CPLD|EEPROM|IPMI|LED|PSU|QSFP|QSFPDD|SFP|UARTMux|USBMux|Thermal|BSP|ROV|INTR|SYSFS|help")

if __name__ == "__main__":
    main()
