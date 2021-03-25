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
from bsp.i2c_mux.i2c_mux import I2CMux
from bsp.gpio.ioexp import IOExpander
from bsp.cpld.cpld import CPLD
from bsp.cpld.cpld_reg import CPLDMBReg
from bsp.eeprom.eeprom import EEPRom
from bsp.thermal.thermal import Thermal
from bsp.utility.intr_utility import INTRUtility
from bsp.utility.rov_utility import ROVUtility
from bsp.protocol.lpc import LPC, LPCDevType
from bsp.utility.bsp_utility import BSPUtility
from time import sleep

class PlatformUtility:

    builtin_pca954x_path = "/lib/modules/{}/kernel/drivers/i2c/muxes/i2c-mux-pca954x.ko"
    #kernel release version
    kr_version_cmd = "uname -r" 
    depmod_cmd = "depmod -a"
    #pci device
    PCI_CHECK_LIST = {
        "00:14.0": "USB controller",
        "00:1d.0": "USB controller",
        "00:1f.2": "SATA controller",
        "00:1f.3": "SMBus",
        "02:00.0": "10 GbE SFP+", 
        "02:00.1": "10 GbE SFP+", 
        "06:00.0": "PEX 8724", 
        "07:01.0": "PEX 8724", 
        "07:02.0": "PEX 8724", 
        "07:08.0": "PEX 8724", 
        "07:09.0": "PEX 8724", 
        "07:0a.0": "PEX 8724", 
        "0b:00.0": "J2", 
        "0c:00.0": "OP2", 
        "0d:00.0": "I210"
        }
    USB_CHECK_LIST = {
        "046b:ff20": "BMC",
        "046b:ff01": "BMC"
        }
    BSP_INIT_STOP = "[BSP Init Stop]"
    IGNORE_ERR = True
    
    def __init__(self):
        try:
            log = Logger(__name__)
            self.logger = log.getLogger()

            # I2C drivers            
            self._load_i2c_drivers()
                        
            #Check Mux Ctrl
            self.lpc = LPC()
            self._check_i2c_mux_ctrl()
            
            self.ioexp = IOExpander()
            
            self.i2c_mux = I2CMux()
            self.eeprom = EEPRom()
            self.cpld = CPLD()
            self.thermal = Thermal()
            self.rov_util = ROVUtility()
            self.intr_util = INTRUtility()
            self.bsp_util = BSPUtility()
        except Exception:
            raise

    def device_init(self):
        try:
            # Unmount kernel modules
            self._unload_kernel_module("gpio_ich")

            # Mount kernel modules
            

            # I2C Mux
            subprocess.run(['modprobe', 'i2c_mux_pca954x', 'force_deselect_on_exit=1'])
            self.i2c_mux.init()

            # EEPROM
            self._load_kernel_module("x86_64_ufispace_s9700_53dx_eeprom_mb")
            self._load_kernel_module("x86_64_ufispace_s9700_53dx_optoe")
            self.eeprom.init()

            # Thermal
            self._load_kernel_module("lm75")
            self.thermal.init()

            # GPIO
            self._load_kernel_module("gpio-pca953x")
            self.ioexp.init(self.i2c_mux.MUXs)
            
            # IPMI
            self._load_kernel_module("ipmi_devintf")
            self._load_kernel_module("ipmi_si")

            # CPLD
            self._load_kernel_module(self.cpld.DRIVER_NAME)
            self.cpld.init()
            
        except Exception:
            raise

    def device_deinit(self):
        try:
            # Remove kernel modules
            # CPLD
            self.cpld.deinit()
            self._unload_kernel_module(self.cpld.DRIVER_NAME)
                        
            # GPIO
            self.ioexp.deinit(self.i2c_mux.MUXs)
            self._unload_kernel_module("gpio-pca953x")

            # Thermal
            self.thermal.deinit()
            self._unload_kernel_module("lm75")

            # MB EEPROM
            self._unload_kernel_module("x86_64_ufispace_s9700_53dx_eeprom_mb")

            # OPTOE EEPROM
            self._unload_kernel_module("x86_64_ufispace_s9700_53dx_optoe")

            # I2C Mux
            self.i2c_mux.deinit()
            self._unload_kernel_module("i2c_mux_pca954x")            
            
        except Exception:
            raise

    def _get_kernel_release(self):
        try:
            return subprocess.getoutput(self.kr_version_cmd)            
        except Exception:
            raise
        
    def _check_bsp_init(self):
        try:
            is_bsp_inited = self.bsp_util.is_bsp_inited()
            
            if is_bsp_inited:
                self.logger.error("BSP may be already initialized. Please run 'platform_utility.py deinit' first")
                self.logger.error(self.BSP_INIT_STOP)
                sys.exit()
        except Exception:
            raise

    def _check_ko(self):
        try:            
            #get kernel release
            kr = self._get_kernel_release()
            
            #remove built-in i2c-mux-pca954x.ko if exist
            pca954x_path = self.builtin_pca954x_path.format(kr)
            if os.path.exists(pca954x_path):                
                os.remove(pca954x_path)
                #generate modules.dep
                subprocess.run(self.depmod_cmd, shell=True)
            
        except Exception:
            raise        

    def check_idt(self):
        try:            
            #Open Mux(0x73) for IDT(0x53)
            retcode, _ = subprocess.getstatusoutput("i2cset -y 0 0x73 0x8")
            if retcode != 0:                
                self.logger.error("Open I2C Mux channel (0x73) for IDT failed.")
                return
            
            #Check IDT
            retcode, _ = subprocess.getstatusoutput("i2cget -y 0 0x53 0x0")
            if retcode != 0:                
                self.logger.error("Access IDT(0x53) failed. Trying to reset IDT")
                
                #Reset IDT
                self.lpc.regSet(LPCDevType.CPLD_ON_MAIN_BOARD, 0x4D, 0xF7)
                sleep(0.5)
                
                #Access IDT again
                retcode, _ = subprocess.getstatusoutput("i2cget -y 0 0x53 0x0")
                if retcode != 0:                
                    self.logger.error("Access IDT(0x53) failed and reset still failed")
                else:
                    self.logger.error("Access IDT(0x53) failed and reset succeed")    
                    
            #Close Mux(0x73)
            retcode, _ = subprocess.getstatusoutput("i2cset -y 0 0x73 0x0")
            if retcode != 0:                
                self.logger.error("Close I2C Mux channel (0x73) failed.")
                        
        except Exception:
            raise
    
    def _check_intr(self):
        try:
            alert_dis = self.intr_util.get_alert_dis()
            if alert_dis == 0:
                self.logger.warning("I2C Alert is already enabled. I2C tree performance may be affected.")       
        except Exception:
            raise

    def _check_i2c_mux_ctrl(self):            
        try:
            default_val = 0x80
            reg_val = self.lpc.regGet(LPCDevType.CPLD_ON_MAIN_BOARD,
                                       CPLDMBReg.REG_MUX_CTRL)
            
            if reg_val != default_val:
                self.logger.error("I2C Mux Ctrl [0x{:02X}] is not valid. Expected [0x{:02X}]".format(reg_val, default_val))
                self.logger.error(self.BSP_INIT_STOP)
                sys.exit()
            else:
                self.logger.info("[Check Mux Control Register] Pass")                
        except Exception as e:
            self.logger.error(e)
            raise   

    def _check_cpld(self):
        
        #CPLD missing workaround :BEGIN

        #open mux 0x75
        retcode, _ = subprocess.getstatusoutput("i2cset -y 0 0x75 0x1")
        if retcode != 0:
            self.logger.error("Open I2C Mux channel 0x75 for CPLD WA failed, return code = {}, exit".format(retcode))
            self.logger.error(self.BSP_INIT_STOP)
            sys.exit()
            
        #Read CPLD version
        for i in range(len(self.cpld.CPLD_I2C_ADDR)):
            retcode, _ = subprocess.getstatusoutput("i2cget -y 0 {} 0x2".format(self.cpld.CPLD_I2C_ADDR[i]))
            if retcode != 0:
                #log info for reading cpld version
                self.logger.info("Reading CPLD{} 0x{:02X} failed".format(i+1, self.cpld.CPLD_I2C_ADDR[i]))
                
        #Check CPLD version
        for i in range(len(self.cpld.CPLD_I2C_ADDR)):
            retcode, _ = subprocess.getstatusoutput("i2cget -y 0 {} 0x2".format(self.cpld.CPLD_I2C_ADDR[i]))
            if retcode != 0:
                #log error for checking cpld version
                self.logger.error("Reading CPLD{} 0x{:02X} failed, return code = {}, exit".format(
                    i+1, self.cpld.CPLD_I2C_ADDR[i], retcode))
                self.logger.error(self.BSP_INIT_STOP)
                sys.exit()
                
        #close mux 0x75
        retcode, _ = subprocess.getstatusoutput("i2cset -y 0 0x75 0x0")
        if retcode != 0:
            self.logger.error("Close I2C Mux channel for CPLD WA failed, return code = {}, exit".format(retcode))
            self.logger.error(self.BSP_INIT_STOP)
            sys.exit()

        #CPLD missing workaround :END
        
        self.logger.info("[Check CPLD] Pass")
        
    def _check_pci(self):        
        err_cnt = 0
        result = ""
        err_list = ["rev ff"]
        err_desc = ["under reset"]
        cmd_lspci = "lspci"
        cmd_lspci_s = "lspci -s {}"
        
        #check lspci command
        retcode, _ = subprocess.getstatusoutput(cmd_lspci)
        if retcode != 0:
            self.logger.warning("lspci commnad not found, skip checking pci devices")            
            return
        
        #check pci devices
        for pci_id in self.PCI_CHECK_LIST.keys():
            pci_name = self.PCI_CHECK_LIST[pci_id]
            retcode, output = subprocess.getstatusoutput(cmd_lspci_s.format(pci_id))
            #check device existence
            if retcode != 0 :
                self.logger.error("Invalid PCI device {} ({}), retcode={}, output={}".format(pci_name, pci_id, retcode, output))
                err_cnt += 1
            elif len(output) == 0 :
                self.logger.error("PCI device {} ({}) not found".format(pci_name, pci_id) )
                if not self.IGNORE_ERR:                
                    self.logger.error(self.BSP_INIT_STOP)
                    sys.exit()
            else:
                #check device error status
                for i in range(len(err_list)):
                    if output.find(err_list[i]) >= 0:
                        self.logger.warning("PCI device {} ({}) {}".format(pci_name, pci_id, err_desc[i]) )
                        err_cnt += 1
        
        if err_cnt == 0:
            result = "Pass"
            self.logger.info("[Check PCI] {}".format(result))            
        else:
            result = "Fail"
            self.logger.warning("[Check PCI] {}".format(result))
    
    def _check_usb(self):        
        warn_cnt = 0
        result = ""
        cmd_lsusb = "lsusb"
        cmd_lsusb_s = "lsusb -d {}"
        
        #check lsusb command
        retcode, _ = subprocess.getstatusoutput(cmd_lsusb)
        if retcode != 0:
            self.logger.warning("cmd_lsusb commnad not found, skip checking usb devices")            
            return
        
        #check usb devices
        for usb_id in self.USB_CHECK_LIST.keys():
            usb_name = self.USB_CHECK_LIST[usb_id]
            retcode, output = subprocess.getstatusoutput(cmd_lsusb_s.format(usb_id))
            #check device existence
            if retcode != 0 :
                self.logger.warning("USB device {} ({}) not found".format(usb_name, usb_id))
                warn_cnt += 1
            elif len(output) == 0 :
                self.logger.warning("USB device {} ({}) not found".format(usb_name, usb_id))
                warn_cnt += 1                
            else:
                if output.find(usb_id) < 0:
                    self.logger.warning("USB device {} ({}) not found".format(usb_name, usb_id))
                    warn_cnt += 1                        
        
        if warn_cnt == 0:
            result = "Pass"
            self.logger.info("[Check USB] {}".format(result))
        else:
            result = "Warning"
            self.logger.warning("[Check USB] {}".format(result))
        return 0
                            
    def pre_init(self):
        self._check_bsp_init()
        # don't check ko for sonic platform
        #self._check_ko()
        self._check_intr()
        retcode = self.i2c_mux.pre_init()
        if retcode != 0:
            self.logger.error(self.BSP_INIT_STOP)
            sys.exit()
        self._check_cpld()
        self.check_idt()
        self._check_pci()
        self._check_usb()
            
    def post_init(self):
        try:
            #set j2 rov
            if self.rov_util.platform_check():
                self.rov_util.set_j2_rov()
        except Exception:
            raise

    def _load_i2c_drivers(self):        
        # I2C I801
        self._load_kernel_module("i2c_i801")
        # I2C Dev
        self._load_kernel_module("i2c_dev")
    
    def _load_kernel_module(self, module_name):
        #replace "-" to "_" since lsmod show module name with "_"
        module_name = module_name.replace("-", "_")

        #check if module is already loaded
        retcode, _ = subprocess.getstatusoutput("lsmod | grep {}".format(module_name))
        #module is not loaded yet
        if retcode != 0:                
            retcode, _ = subprocess.getstatusoutput("modprobe {}".format(module_name))
            #load module failed
            if retcode != 0:
                self.logger.error("Load kernel module {} failed, retcode={}".format(module_name, retcode))
                if not self.IGNORE_ERR:                                    
                    self.logger.error(self.BSP_INIT_STOP)
                    sys.exit()
                
    def _unload_kernel_module(self, module_name):
        #replace "-" to "_" since lsmod show module name with "_"
        module_name = module_name.replace("-", "_")

        #check if module is already loaded
        retcode, _ = subprocess.getstatusoutput("lsmod | grep {}".format(module_name))
        #module is loaded
        if retcode == 0:                
            retcode, _ = subprocess.getstatusoutput("rmmod {}".format(module_name))
            #unload module failed
            if retcode != 0:
                self.logger.error("Unload kernel module {} failed, retcode={}".format(module_name, retcode))    

def main():
    util = PlatformUtility()

    if len(sys.argv) != 2:
        print("\nUsage: sudo " + sys.argv[0] + " init|deinit|pre_init")
        return

    if sys.argv[1] == 'init':
        util.pre_init()
        util.device_init()
        util.post_init()
    elif sys.argv[1] == 'deinit':
        util.device_deinit()
    elif sys.argv[1] == 'pre_init':
        util.pre_init()        
    else:
        print("Invalid arguments:")

        # print command line arguments
        for arg in sys.argv[1:]:
            print(arg)
        print("\nUsage: sudo " + sys.argv[0] + " init|deinit|pre_init")

if __name__ == "__main__":
    main()
