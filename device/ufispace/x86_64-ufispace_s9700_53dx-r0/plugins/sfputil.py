# sfputil.py
#
# Platform-specific SFP transceiver interface for SONiC
#

import os
import subprocess
import re


try:
    import time
    from sonic_sfp.sfputilbase import SfpUtilBase
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))


class SfpUtil(SfpUtilBase):
    """Platform-specific SfpUtil class"""

    PORT_START = 0
    PORT_END = 52
    PORTS_IN_BLOCK = 53
    QSFP_PORT_END = 39
    QSFPDD_PORT_START = QSFP_PORT_END + 1

    _port_to_eeprom_mapping = {}

    @property
    def port_start(self):
        return self.PORT_START

    @property
    def port_end(self):
        return self.PORT_END

    @property
    def qsfp_ports(self):
        return range(0, self.PORTS_IN_BLOCK + 1)

    @property
    def port_to_eeprom_mapping(self):
        return self._port_to_eeprom_mapping

    def _qsfp_get_bus_num(self, port):
        ret_code = 0
        bus_num = 0
        out = subprocess.Popen(['bsp_ut.py', 'EEPROM', '6', str(port)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            ret_code = out.returncode
            return ret_code, bus_num

        stdout_str = stdout.decode("utf-8").rstrip()
        return ret_code, int(stdout_str)

    def _qsfpdd_get_bus_num(self, port):
        ret_code = 0
        bus_num = 0
        out = subprocess.Popen(['bsp_ut.py', 'EEPROM', '7', str(port)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            ret_code = out.returncode
            return ret_code, bus_num

        stdout_str = stdout.decode("utf-8").rstrip()
        return ret_code, int(stdout_str)

    def __init__(self):

        # Override port_to_eeprom_mapping for class initialization
        eeprom_path = '/sys/class/i2c-adapter/i2c-{0}/{0}-0050/eeprom'

        # QSFP port eeprom path setting
        for x in range(self.port_start, self.QSFPDD_PORT_START):
            port = x
            ret, bus_num = self._qsfp_get_bus_num(port)
            if ret != 0:
                print("get qsfp port {0} bus num failed".format(port))
            else:
                port_eeprom_path = eeprom_path.format(bus_num)
                self.port_to_eeprom_mapping[x] = port_eeprom_path

        # QSFPDD port eeprom path setting
        for x in range(self.QSFPDD_PORT_START, self.PORTS_IN_BLOCK):
            port = x-self.QSFPDD_PORT_START
            ret, bus_num = self._qsfpdd_get_bus_num(port)
            if ret != 0:
                print("get qsfpdd port {0} bus num failed".format(port))
            else:
                port_eeprom_path = eeprom_path.format(bus_num)
                self.port_to_eeprom_mapping[x] = port_eeprom_path

        SfpUtilBase.__init__(self)

    def _get_qsfp_presence(self, port_num):
        out = subprocess.Popen(['bsp_ut.py', 'QSFP', '1', str(port_num)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        status_str = re.search(r'{\'presence\': \'(\w*)\'}', stdout_str, re.M | re.I).group(1)
        if status_str == 'presence':
            return True

        return False

    def _get_qsfpdd_presence(self, port_num):
        out = subprocess.Popen(['bsp_ut.py', 'QSFPDD', '1', str(port_num)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        status_str = re.search(r'{\'presence\': \'(\w*)\'}', stdout_str, re.M | re.I).group(1)
        if status_str == 'presence':
            return True

        return False

    def get_presence(self, port_num):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        # QSFP port presence
        if port_num >= self.port_start and port_num <= self.QSFP_PORT_END:
            return self._get_qsfp_presence(port_num)
        # QSFPDD port presence
        else :
            return self._get_qsfpdd_presence(port_num - self.QSFPDD_PORT_START)

    def _get_qsfp_lp_mode(self, port_num):
        out = subprocess.Popen(['bsp_ut.py', 'QSFP', '2', str(port_num)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        status_str = re.search(r'{\'lp_mode\': \'(\w*)\'}', stdout_str, re.M | re.I).group(1)
        if status_str == 'enabled':
            return True

        return False

    def _get_qsfpdd_lp_mode(self, port_num):
        out = subprocess.Popen(['bsp_ut.py', 'QSFPDD', '2', str(port_num)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        status_str = re.search(r'{\'lp_mode\': \'(\w*)\'}', stdout_str, re.M | re.I).group(1)
        if status_str == 'enabled':
            return True

        return False

    def get_low_power_mode(self, port_num):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        # QSFP port lp mode status
        if port_num >= self.port_start and port_num <= self.QSFP_PORT_END:
            return self._get_qsfp_lp_mode(port_num)
        # QSFPDD port lp mode status
        else :
            return self._get_qsfpdd_lp_mode(port_num - self.QSFPDD_PORT_START)

    def _set_qsfp_lp_mode(self, port_num, enable):

        out = subprocess.Popen(['bsp_ut.py', 'QSFP', '3', str(port_num), str(enable)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        if not status_str:
            # output result error
            return False

        return True

    def _set_qsfpdd_lp_mode(self, port_num, enable):
        out = subprocess.Popen(['bsp_ut.py', 'QSFPDD', '3', str(port_num), str(enable)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        if not status_str:
            # output result error
            return False

        return True

    def set_low_power_mode(self, port_num, lpmode):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        if lpmode is True:
            val = 1
        else :
            val = 0

        # QSFP set lp mode
        if port_num >= self.port_start and port_noum <= self.QSFP_PORT_END:
            return self._set_qsfp_lp_mode(port_num, val)
        # QSFPDD set lp mode
        else :
            return self._set_qsfpdd_lp_mode(port_num - self.QSFPDD_PORT_START, val)

    def _qsfp_reset_port(self, port_num):

        out = subprocess.Popen(['bsp_ut.py', 'QSFP', '5', str(port_num)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        if not stdout_str:
            # output result error
            return False

        return True

    def _qsfpdd_reset_port(self, port_num):
        out = subprocess.Popen(['bsp_ut.py', 'QSFPDD', '5', str(port_num)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return False

        stdout_str = stdout.decode("utf-8").rstrip()
        if not stdout_str:
            # output result error
            return False

        return True

    def reset(self, port_num):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        # QSFP reset port
        if port_num >= self.port_start and port_noum <= self.QSFP_PORT_END:
            return self._qsfp_reset_port(port_num)
        # QSFPDD reset port
        else :
            return self._qsfpdd_reset_port(port_num - self.QSFPDD_PORT_START)

    def get_transceiver_change_event(self):
        """
        TODO: This function need to be implemented
        when decide to support monitoring SFP(Xcvrd)
        on this platform.
        """
        raise NotImplementedError
