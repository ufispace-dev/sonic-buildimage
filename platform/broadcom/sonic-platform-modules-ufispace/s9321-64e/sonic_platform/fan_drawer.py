#!/usr/bin/env python


try:
    from sonic_platform_pddf_base.pddf_fan_drawer import PddfFanDrawer
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class FanDrawer(PddfFanDrawer):
    """PDDF Platform-Specific Fan-Drawer class"""

    def __init__(self, tray_idx, pddf_data=None, pddf_plugin_data=None):
        # idx is 0-based 
        PddfFanDrawer.__init__(self, tray_idx, pddf_data, pddf_plugin_data)

    # Provide the functions/variables below for which implementation is to be overwritten

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device

        Returns:
            string: Model/part number of device
        """
        attr_name= "fantray{}_model_name".format(self.fantray_index)
        output = self.pddf_obj.get_attr_name_output("FAN-CTRL", attr_name)
        if not output:
            return None

        model = output['status']

        # strip_non_ascii
        stripped = (c for c in model if 0 < ord(c) < 127)
        model = ''.join(stripped)

        return model.rstrip('\n')

    def get_serial(self):
        """
        Retrieves the serial number of the device

        Returns:
            string: Serial number of device
        """
        attr_name= "fantray{}_serial_num".format(self.fantray_index)
        output = self.pddf_obj.get_attr_name_output("FAN-CTRL", attr_name)
        if not output:
            return None

        serial = output['status']

        # strip_non_ascii
        stripped = (c for c in serial if 0 < ord(c) < 127)
        serial = ''.join(stripped)

        return serial.rstrip('\n')