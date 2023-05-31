#!/bin/bash
#echo 1 > /sys/kernel/pddf/devices/sysstatus/sysstatus_data/port_led_clr_ctrl

#disable bmc watchdog
timeout 3 ipmitool mc watchdog off

#set status led to green to indicate platform init done
pddf_ledutil setstatusled SYS_LED green

echo "PDDF device post-create completed"
