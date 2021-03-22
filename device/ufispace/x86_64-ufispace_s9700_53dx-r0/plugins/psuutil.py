#
# psuutil.py
# Platform-specific PSU status interface for SONiC
#


import os.path
import subprocess
import re
try:
    from sonic_psu.psu_base import PsuBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class PsuUtil(PsuBase):
    """Platform-specific PSUutil class"""

    def __init__(self):
        PsuBase.__init__(self)

    def get_num_psus(self):
        """
        Retrieves the number of PSUs available on the device
        :return: An integer, the number of PSUs available on the device
         """
        MAX_PSUS = 2
        return MAX_PSUS

    def get_psu_status(self, index):
        """
        Retrieves the oprational status of power supply unit (PSU) defined
                by index <index>
        :param index: An integer, index of the PSU of which to query status
        :return: Boolean, True if PSU is operating properly, False if PSU is\
        faulty
        """
        status = 0
        psu_index = index - 1
        out = subprocess.Popen(['bsp_ut.py', 'PSU', '2', str(psu_index)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return 0

        stdout_str = stdout.decode("utf-8").rstrip()
        status_str = re.search( r'{\'power\': \'(\w*)\'}', stdout_str, re.M|re.I).group(1)
        if status_str == 'ok':
            status = 1

        return status

    def get_psu_presence(self, index):
        """
        Retrieves the presence status of power supply unit (PSU) defined
                by index <index>
        :param index: An integer, index of the PSU of which to query status
        :return: Boolean, True if PSU is plugged, False if not
        """
        status = 0
        psu_index = index - 1
        out = subprocess.Popen(['bsp_ut.py', 'PSU', '1', str(psu_index)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode != 0:
            # command not success
            return 0

        stdout_str = stdout.decode("utf-8").rstrip()
        status_str = re.search( r'{\'presence\': \'(\w*)\'}', stdout_str, re.M|re.I).group(1)
        if status_str == 'presence':
            status = 1

        return status

