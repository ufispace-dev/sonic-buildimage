#!/bin/bash

set -exuo pipefail

COLOR_TITLE="\033[45;38m"
COLOR_ERROR="\033[41;30m"
COLOR_PASS="\033[42;30m"
COLOR_WARNING="\033[43;30m"
COLOR_END="\033[0m"

ROOT_DIR="$(cd "$(dirname "$0")/../../../../" && pwd)"
PATCH_DIR="${ROOT_DIR}/files/ufi/patch/ztp"

function _make_init {
    echo -e "${COLOR_TITLE} ==== ${FUNCNAME[0]} ==== ${COLOR_END}"

    cd ${ROOT_DIR}/
    if [ ! -f "${ROOT_DIR}/.init" ]; then
        if [ ! -f "${ROOT_DIR}/src/sonic-linux-kernel/.git" ]; then
            make init
        fi
        touch ${ROOT_DIR}/.init
    fi

    echo -e "${COLOR_PASS} ${FUNCNAME[0]}: PASS ${COLOR_END}"
}

function _ztp_patch {
    echo -e "${COLOR_TITLE} ==== ${FUNCNAME[0]} ${1} ==== ${COLOR_END}"

    if [ ! -f "${ROOT_DIR}/src/sonic-linux-kernel/.git" ]; then
        echo -e "${COLOR_ERROR} ERROR!! Please run 'make init' first to download the submodule for patch!! ${COLOR_END}"
        echo -e "${COLOR_ERROR} ERROR!! Please run 'make init' first to download the submodule for patch!! ${COLOR_END}"
        echo -e "${COLOR_ERROR} ERROR!! Please run 'make init' first to download the submodule for patch!! ${COLOR_END}"
        sleep 60
        exit 1
    fi

    # If the CHECK is empty, it will apply the patch; otherwise (--check), it will only verify whether the patch is correct.
    CHECK="$1"
    if [ ! -f "${ROOT_DIR}/.patch.ztp" ]; then

        # patch to add support for ztp inband port feature
        cd ${ROOT_DIR}/ && git apply ${CHECK} ${PATCH_DIR}/0001-sonic-buildimage-add-support-for-ztp-inband.patch
        cd ${ROOT_DIR}/src/sonic-swss/ && git apply ${CHECK} ${PATCH_DIR}/0001-sonic-swss-add-support-for-ztp-inband.patch
        cd ${ROOT_DIR}/src/sonic-utilities/ && git apply ${CHECK} ${PATCH_DIR}/0001-sonic-utilities-add-support-for-ztp-inband.patch
        cd ${ROOT_DIR}/src/sonic-ztp/ && git apply ${CHECK} ${PATCH_DIR}/0001-sonic-ztp-add-support-for-ztp-inband.patch
        cd ${ROOT_DIR}/

        if [ "${CHECK}" = "--check" ]; then
            touch ${ROOT_DIR}/.check.ztp
        elif [ -z "${CHECK}" ]; then
            touch ${ROOT_DIR}/.patch.ztp
        fi
    fi

    echo -e "${COLOR_PASS} ${FUNCNAME[0]} ${1}: PASS ${COLOR_END}"
}

function _make_configure {
    echo -e "${COLOR_TITLE} ==== ${FUNCNAME[0]} ==== ${COLOR_END}"

    cd ${ROOT_DIR}/
    if [ ! -f "${ROOT_DIR}/.configure" ]; then
        time make PLATFORM=broadcom SONIC_IMAGE_VERSION="sonic-${PWD##*/}" configure
        touch ${ROOT_DIR}/.configure
    fi

    echo -e "${COLOR_PASS} ${FUNCNAME[0]}: PASS ${COLOR_END}"
}

function _build_image {
    echo -e "${COLOR_TITLE} ==== ${FUNCNAME[0]} ==== ${COLOR_END}"

    set +e
    cd ${ROOT_DIR}/
    time make SONIC_BUILD_JOBS=8 target/sonic-broadcom.bin
    
    if [ -f "${ROOT_DIR}/target/sonic-broadcom.bin" ]; then
        echo -e "${COLOR_PASS} ${FUNCNAME[0]}: PASS ${COLOR_END}"
    else
        echo -e "${COLOR_ERROR} ${FUNCNAME[0]}: FAIL ${COLOR_END}"
    fi
}

function _rebuild_image {
    echo -e "${COLOR_TITLE} ==== ${FUNCNAME[0]} ==== ${COLOR_END}"

    set +e
    cd ${ROOT_DIR}/
    if [ ! -f "target/sonic-broadcom.bin" ]; then
        touch .first_time_build_failed
        echo "###############################################################"
        echo "###############################################################"
        echo "###############################################################"
        echo "###############################################################"
        echo "###############################################################"
        echo "###############################################################"
        echo "sleep 600 seconds...."
        for (( i=0;i<60;i++ )); do
            echo -n "."
            sleep 10
        done
        time make target/sonic-broadcom.bin
    fi
    
    if [ -f "${ROOT_DIR}/target/sonic-broadcom.bin" ]; then
        echo -e "${COLOR_PASS} ${FUNCNAME[0]}: PASS ${COLOR_END}"
    else
        echo -e "${COLOR_ERROR} ${FUNCNAME[0]}: FAIL ${COLOR_END}"
    fi
}

function _main {
    echo -e "${COLOR_TITLE} ==== ${FUNCNAME[0]} ==== ${COLOR_END}"

    codename_array=($@)

    if [ ${#codename_array[@]} == 0 ]; then
        _ztp_patch "--check"
        _ztp_patch ""
    elif [ "${codename_array[0]}" == "build" ]; then
        _make_init
        _ztp_patch "--check"
        _ztp_patch ""
        _make_configure
        _build_image
        _rebuild_image
    else
        _ztp_patch "--check"
        _ztp_patch ""
    fi
    set +e
}

_main $@
