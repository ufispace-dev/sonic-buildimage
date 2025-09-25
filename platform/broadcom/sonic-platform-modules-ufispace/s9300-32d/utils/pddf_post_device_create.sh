#!/bin/bash
#disable bmc watchdog
timeout 3 ipmitool mc watchdog off

#set bmc sel time
echo "Set BMC SEL time to system time"
timeout 5 ipmitool sel time set now > /dev/null 2>&1

echo 1 > /sys/kernel/pddf/devices/sysstatus/sysstatus_data/port_led_clr_ctrl
echo "PDDF device post-create completed"
