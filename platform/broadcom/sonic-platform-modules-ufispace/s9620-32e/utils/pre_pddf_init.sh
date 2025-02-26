#!/bin/bash

# Import SONiC environment
[ -f /etc/sonic/sonic-environment ] && . /etc/sonic/sonic-environment

TRUE=0
FALSE=1

# Hardware revision definitions
PROTO=0
ALPHA=1
BETA=2
PVT=3

PLATFORM=${PLATFORM:-x86_64-ufispace_s9620_32e-r0}
HWSKU=${HWSKU:-UFISPACE-S9620-32E}
DEV_BASE="/usr/share/sonic/device/$PLATFORM"
BCM_CONF_FILE_PATH="$DEV_BASE/$HWSKU"
PDDF_BASE="$DEV_BASE/pddf"
IO_PORT_FILE="/dev/port"

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

# Function to detect hardware revision ID
function check_hw_rev_id {
    if _check_filepath "$IO_PORT_FILE"; then
        if ! REG=$(xxd -s 0xE01 -p -l 1 -c 1 "$IO_PORT_FILE" 2>/dev/null); then
            echo "[ERR] Failed to read from $IO_PORT_FILE"
            HW_REV_ID=$BETA
        else
            MASK=0x03
            HW_REV_ID=$(( 0x$REG & MASK ))
        fi
    else
        HW_REV_ID=$BETA
    fi
    echo "HW_REV_ID detected: $HW_REV_ID"
}

# Function to configure device JSON file
function config_device {
    local src
    case $HW_REV_ID in
        $BETA) src="$PDDF_BASE/pddf-device-beta.json" ;;
        *)     src="$PDDF_BASE/pddf-device-alpha.json" ;;
    esac
    _check_filepath "$src" && ln -rsf "$src" "$PDDF_BASE/pddf-device.json"
}

# Function to configure platform JSON files
function config_platform_files {
    local src_platform src_platform_components
    case $HW_REV_ID in
        $BETA)
            src_platform="$DEV_BASE/platform-beta.json"
            src_platform_components="$DEV_BASE/platform_components-beta.json"
            ;;
        *)
            src_platform="$DEV_BASE/platform-alpha.json"
            src_platform_components="$DEV_BASE/platform_components-alpha.json"
            ;;
    esac
    _check_filepath "$src_platform" && ln -rsf "$src_platform" "$DEV_BASE/platform.json"
    _check_filepath "$src_platform_components" && ln -rsf "$src_platform_components" "$DEV_BASE/platform_components.json"
}

# Function to configure BCM file
function config_bcm_file {
    local src_bcm_file
    case $HW_REV_ID in
        $BETA) src_bcm_file="$BCM_CONF_FILE_PATH/q3d-s9620-32e-32x800G-beta.config" ;;
        *)     src_bcm_file="$BCM_CONF_FILE_PATH/q3d-s9620-32e-32x800G-alpha.config" ;;
    esac
    if _check_filepath "$src_bcm_file"; then
        ln -rsf "$src_bcm_file" "$BCM_CONF_FILE_PATH/q3d-s9620-32e-32x800G.config"
        ln -rsf "$src_bcm_file" "$BCM_CONF_FILE_PATH/q3d-s9620-32e-32x800G.config.bcm"
    fi
}

# Execute functions
check_hw_rev_id
config_device
config_platform_files
config_bcm_file

echo "PDDF/PLATFORM/CONFIG pre-init completed"
