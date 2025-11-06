#!/bin/bash

# import sonic env
[ -f /etc/sonic/sonic-environment ] && . /etc/sonic/sonic-environment

TRUE=0
FALSE=1

SKU_POE=0
SKU_NPOE_0BASE=1
SKU_NPOE_1BASE=2
SKU_POE_1PSU=3

PLATFORM=${PLATFORM:-x86_64-ufispace_s6301_56stp-r0}
PDDF_DEV_PATH="/usr/share/sonic/device/$PLATFORM/pddf"
PDDF_DEV_FILE="/usr/share/sonic/device/$PLATFORM/pddf/pddf-device.json"
IO_PORT_FILE="/dev/port"

function _check_filepath {
    filepath=$1
    if [ -z "${filepath}" ]; then
        echo "[ERR] the ipnut string is empty!!!"
        return ${FALSE}
    elif [ ! -f "$filepath" ] && [ ! -c "$filepath" ]; then
        echo "[ERR] No such file: ${filepath}"
        return ${FALSE}
    else
        return ${TRUE}
    fi
}

if _check_filepath "$IO_PORT_FILE" ; then
   MASK=2#00000111
   REG="0x$(xxd -s 0x706 -p -l 1 -c 1 /dev/port)"
   HW_EXT_ID=$(( $REG & $MASK ))
else
   HW_EXT_ID=$SKU_POE
fi

if [ "$HW_EXT_ID" -eq "$SKU_POE_1PSU" ]; then

   src="$PDDF_DEV_PATH/pddf-device-ext.json"
   if _check_filepath "$src"; then
         ln -rsf "$src" "$PDDF_DEV_FILE"
   fi
else
   src="$PDDF_DEV_PATH/pddf-device-org.json"
   if _check_filepath "$src"; then
         ln -rsf "$src" "$PDDF_DEV_FILE"
   fi
fi
