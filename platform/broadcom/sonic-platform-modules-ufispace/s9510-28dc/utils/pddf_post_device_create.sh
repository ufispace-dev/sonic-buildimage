#!/bin/bash

#disable bmc watchdog
echo "Disable BMC watchdog"
timeout 3 ipmitool mc watchdog off

#set bmc sel time
echo "Set BMC SEL time to system time"
timeout 5 ipmitool sel time set now > /dev/null 2>&1

printf "Set GNSS_LED off %s\n" "$(pddf_ledutil setstatusled GNSS_LED off)"
printf "Set SYNC_LED off %s\n" "$(pddf_ledutil setstatusled SYNC_LED off)"
printf "Set SYS_LED off %s\n" "$(pddf_ledutil setstatusled SYS_LED off)"
printf "Set SYS_LED %s to green %s\n" "$(pddf_ledutil getstatusled SYS_LED)" "$(pddf_ledutil setstatusled SYS_LED green)"

echo "PDDF device post-create completed"
