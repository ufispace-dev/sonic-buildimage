#!/bin/bash

# import sonic env
[ -f /etc/sonic/sonic-environment ] && . /etc/sonic/sonic-environment

TRUE=0
FALSE=1

PLATFORM=${PLATFORM:-x86_64-ufispace_s9510_28dc-r0}
HWSKU=${HWSKU:-UFISPACE-S9510-28DC}
BCM_CONF_FILE="/usr/share/sonic/device/$PLATFORM/$HWSKU/q2a-s9510-28dc.config"
BCM_CONF_BCM_FILE="$BCM_CONF_FILE.bcm"

function _check_filepath {
    filepath=$1
    silent="${2:-0}" 

    if [ -z "${filepath}" ]; then
        if [ "$silent" = "0" ]; then
            echo "[ERR] the ipnut string is empty!!!"
        fi
        return ${FALSE}
    elif [ ! -f "$filepath" ]; then
        if [ "$silent" = "0" ]; then
            echo "[ERR] No such file: ${filepath}"
        fi
        return ${FALSE}
    else
        #_echo "File Path: ${filepath}"
        return ${TRUE}
    fi
}

if _check_filepath $BCM_CONF_FILE 1; then
      mv "$BCM_CONF_FILE" "$BCM_CONF_BCM_FILE"
fi