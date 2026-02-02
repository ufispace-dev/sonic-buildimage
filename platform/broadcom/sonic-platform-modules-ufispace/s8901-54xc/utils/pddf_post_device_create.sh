#!/bin/bash

TRUE=0
FALSE=1

HW_EXT_ID=-1
NTM_PRESENCE=0
IO_PORT_FILE="/dev/port"

# Hardware ext id definitions
EXT_ID_0=0
EXT_ID_1=1

# Function to check file existence
function _check_filepath {
    local filepath=$1
    if [ -z "$filepath" ]; then
        echo "[ERR] The input string is empty!"
        return $FALSE
    elif [ ! -f "$filepath" ] && [ ! -c "$filepath" ]; then
        echo "[ERR] No such file: $filepath"
        return $FALSE
    else
        return $TRUE
    fi
}

# Function to detect hardware ext ID
function check_hw_ext_id {
    if _check_filepath "$IO_PORT_FILE"; then
        if ! REG=$(xxd -s 0x706 -p -l 1 -c 1 "$IO_PORT_FILE" 2>/dev/null); then
            echo "[ERR] Failed to read from $IO_PORT_FILE"
            HW_EXT_ID=-1
        else
            MASK=0x07
            HW_EXT_ID=$(( 0x$REG & MASK ))
        fi
    else
        HW_EXT_ID=-1
    fi
    echo "HW_EXT_ID detected: $HW_EXT_ID"
}

# Function to check NTM presence
function check_ntm_presence {
    check_hw_ext_id
    if [ "$HW_EXT_ID" -eq "$EXT_ID_0" ] || [ "$HW_EXT_ID" -eq "$EXT_ID_1" ]; then
        NTM_PRESENCE=1
    else
        NTM_PRESENCE=0
    fi
}

#disable bmc watchdog
echo "Disable BMC watchdog"
timeout 3 ipmitool mc watchdog off

#set bmc sel time
echo "Set BMC SEL time to system time"
timeout 5 ipmitool sel time set now > /dev/null 2>&1

check_ntm_presence
if [ "$NTM_PRESENCE" -eq 1 ]; then
    pddf_ledutil setstatusled DIAG_LED off
fi

pddf_ledutil setstatusled SYS_LED off
pddf_ledutil setstatusled LOC_LED off

#set status led to green to indicate platform init done
curr_led=$(pddf_ledutil getstatusled SYS_LED)
pddf_ledutil setstatusled SYS_LED green
echo "Set SYS_LED from $curr_led to green"

echo "PDDF device post-create completed"
