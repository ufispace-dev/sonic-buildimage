#!/bin/bash

set -exuo pipefail

COLOR_TITLE="\033[45;38m"
COLOR_ERROR="\033[41;30m"
COLOR_PASS="\033[42;30m"
COLOR_WARNING="\033[43;30m"
COLOR_END="\033[0m"

log_title() { echo -e "${COLOR_TITLE} $* ${COLOR_END}"; }
log_pass() { echo -e "${COLOR_PASS}PASS:${COLOR_END} $*"; }
log_warn() { echo -e "${COLOR_WARNING}WARN:${COLOR_END} $*"; }
log_err()  { echo -e "${COLOR_ERROR}ERROR:${COLOR_END} $*" >&2; }

ROOT_DIR="$(cd "$(dirname "$0")/../../../../" && pwd)"
PATCH_DIR="${ROOT_DIR}/files/ufi/patch/poe"

function _make_init {
    log_title "==== ${FUNCNAME[0]} ===="

    cd ${ROOT_DIR}/
    if [ ! -f "${ROOT_DIR}/.init" ]; then
        if [ ! -f "${ROOT_DIR}/src/sonic-linux-kernel/.git" ]; then
            make init
        fi
        touch ${ROOT_DIR}/.init
    fi

    log_pass "${FUNCNAME[0]}"
}

function _poe_patch {
    log_title "==== ${FUNCNAME[0]} ${1} ===="

    if [ ! -f "${ROOT_DIR}/src/sonic-linux-kernel/.git" ]; then
        log_err "Please run 'make init' first to download the submodule for patch!!"
        log_err "Please run 'make init' first to download the submodule for patch!!"
        log_err "Please run 'make init' first to download the submodule for patch!!"
        sleep 60
        exit 1
    fi

    # If the CHECK is empty, it will apply the patch; otherwise (--check), it will only verify whether the patch is correct.
    CHECK="$1"
    if [ ! -f "${ROOT_DIR}/.patch.poe" ]; then

        # required file list
        # 1. sonic-buildimage/files/ufi/lib/libsaiufi_amd64.deb
        # 2.1. device/ufispace/poe-platform/context_config.json
        # 2.2. device/ufispace/poe-platform/poe_config.json
        # 2.3. device/ufispace/poe-platform/poe.profile
        [ -z "${CHECK}" ] && cp -rf ${ROOT_DIR}/files/ufi/patch/poe/sonic-buildimage/* ${ROOT_DIR}/
        
        # patch to add support for PoE feature
        cd ${ROOT_DIR}/ && git apply ${CHECK} ${PATCH_DIR}/0001-sonic_buildimage_add_broadcom_poesyncd.patch
        cd ${ROOT_DIR}/ && git apply ${CHECK} ${PATCH_DIR}/sonic_buildimage_0_19636_add_support_for_poe_feature.patch
        cd ${ROOT_DIR}/ && git apply ${CHECK} ${PATCH_DIR}/sonic_buildimage_1_21005_add_yang_model_for_poe_port.patch
        cd ${ROOT_DIR}/src/sonic-sairedis/ && git apply ${CHECK} ${PATCH_DIR}/sonic_sairedis_0_1404_add_support_for_poe_feature.patch
        cd ${ROOT_DIR}/src/sonic-swss/ && git apply ${CHECK} ${PATCH_DIR}/sonic_swss_0_3238_add_support_for_poe_feature.patch
        cd ${ROOT_DIR}/src/sonic-swss-common/ && git apply ${CHECK} ${PATCH_DIR}/sonic_swss_common_0_894_add_additional_tables_to_support_poe_feature.patch
        cd ${ROOT_DIR}/src/sonic-utilities/ && git apply ${CHECK} ${PATCH_DIR}/sonic_utilities_0_3436_add_poe_cli.patch
        cd ${ROOT_DIR}/

        if [ "${CHECK}" = "--check" ]; then
            touch ${ROOT_DIR}/.check.poe
        elif [ -z "${CHECK}" ]; then
            touch ${ROOT_DIR}/.patch.poe
        fi
    fi

    log_pass "${FUNCNAME[0]} ${1}"
}

function _make_configure {
    log_title "==== ${FUNCNAME[0]} ===="

    cd ${ROOT_DIR}/
    if [ ! -f "${ROOT_DIR}/.configure" ]; then
        time make PLATFORM=broadcom SONIC_IMAGE_VERSION="sonic-${PWD##*/}" configure
        touch ${ROOT_DIR}/.configure
    fi

    log_pass "${FUNCNAME[0]}"
}

function _build_image {
    log_title "==== ${FUNCNAME[0]} ===="

    set +e
    cd ${ROOT_DIR}/
    time make SONIC_BUILD_JOBS=8 BUILD_SKIP_TEST=y target/sonic-broadcom.bin
    
    if [ -f "${ROOT_DIR}/target/sonic-broadcom.bin" ]; then
        log_pass "${FUNCNAME[0]}"
    else
        log_err "${FUNCNAME[0]}"
    fi
}

function _rebuild_image {
    log_title "==== ${FUNCNAME[0]} ===="

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
        time make BUILD_SKIP_TEST=y target/sonic-broadcom.bin
    fi
    
    if [ -f "${ROOT_DIR}/target/sonic-broadcom.bin" ]; then
        log_pass "${FUNCNAME[0]}"
    else
        log_err "${FUNCNAME[0]}"
    fi
}

function _main {
    log_title "==== ${FUNCNAME[0]} ===="

    codename_array=($@)

    if [ ${#codename_array[@]} == 0 ]; then
        _poe_patch "--check"
        _poe_patch ""
    elif [ "${codename_array[0]}" == "build" ]; then
        rm -rf ${ROOT_DIR}/.make_done
        _make_init
        _poe_patch "--check"
        _poe_patch ""
        _make_configure
        _build_image
        _rebuild_image
        touch ${ROOT_DIR}/.make_done
    else
        _poe_patch "--check"
        _poe_patch ""
    fi
    set +e
}

_main $@
