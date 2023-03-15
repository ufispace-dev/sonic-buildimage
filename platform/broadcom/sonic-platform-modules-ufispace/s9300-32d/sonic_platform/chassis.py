#!/usr/bin/env python

#############################################################################
# PDDF
# Module contains an implementation of SONiC Chassis API
#
#############################################################################

try:
    import time
    from sonic_platform_pddf_base.pddf_chassis import PddfChassis
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

NUM_COMPONENT = 5

class Chassis(PddfChassis):
    """
    PDDF Platform-specific Chassis class
    """

    SFP_STATUS_INSERTED = "1"
    SFP_STATUS_REMOVED = "0"
    port_dict = {}

    def __init__(self, pddf_data=None, pddf_plugin_data=None):
        PddfChassis.__init__(self, pddf_data, pddf_plugin_data)
        self._initialize_components()

    def _initialize_components(self):
        from sonic_platform.component import Component
        for index in range(NUM_COMPONENT):
            component = Component(index)
            self._component_list.append(component)
            
    # Provide the functions/variables below for which implementation is to be overwritten
    def initizalize_system_led(self):
        return True

    def get_status_led(self):
        return self.get_system_led("SYS_LED")

    def get_change_event(self, timeout=0):
        change_event_dict = {"fan": {}, "sfp": {}} 
        sfp_status, sfp_change_dict = self.get_transceiver_change_event(timeout)
        change_event_dict["sfp"] = sfp_change_dict
        if sfp_status is True:
            return True, change_event_dict

        return False, {}

    def get_transceiver_change_event(self, timeout=0):
        start_time = time.time()
        currernt_port_dict = {}
        forever = False

        if timeout == 0:
            forever = True
        elif timeout > 0:
            timeout = timeout / float(1000)  # Convert to secs
        else:
            print("get_transceiver_change_event:Invalid timeout value", timeout)
            return False, {}

        end_time = start_time + timeout
        if start_time > end_time:
            print(
                "get_transceiver_change_event:" "time wrap / invalid timeout value",
                timeout,
            )   
            return False, {}  # Time wrap or possibly incorrect timeout

        while timeout >= 0:
            # Check for OIR events and return updated port_dict
            for index in range(self.platform_inventory['num_ports']):
                if self._sfp_list[index].get_presence():
                    currernt_port_dict[index] = self.SFP_STATUS_INSERTED
                else:
                    currernt_port_dict[index] = self.SFP_STATUS_REMOVED
            if currernt_port_dict == self.port_dict:
                if forever:
                    time.sleep(1)
                else:
                    timeout = end_time - time.time()
                    if timeout >= 1:
                        time.sleep(1)  # We poll at 1 second granularity
                    else:
                        if timeout > 0:
                            time.sleep(timeout)
                        return True, {}
            else:
                # Update reg value
                self.port_dict = currernt_port_dict
                return True, self.port_dict
        print("get_transceiver_change_event: Should not reach here.")
        return False, {}

    def get_sfp(self, index):
        """
        Retrieves sfp represented by (1-based) index <index>

        Args:
            index: An integer, the index (1-based) of the sfp to retrieve.
            The index should be the sequence of a physical port in a chassis,
            starting from 1.
            For example, 1 for Ethernet0, 2 for Ethernet4 and so on.

        Returns:
            An object derived from SfpBase representing the specified sfp
        """
        sfp = None

        try:
            # The index will start from 1
            # sfputil already convert to physical port index according to config
            sfp = self._sfp_list[index]
        except IndexError:
            sys.stderr.write("SFP index {} out of range (1-{})\n".format(
                             index, len(self._sfp_list)))
        return sfp
