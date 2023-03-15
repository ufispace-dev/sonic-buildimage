#!/bin/bash
#
#
# Copyright 2019 UfiSpace Co.,Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Generate Sysdump
# creates a snapshot of system state for debugging later.
#

set -u

ERROR_TAR_FAILED=5
ERROR_PROCFS_SAVE_FAILED=6
ERROR_INVALID_ARGUMENT=10

TAR=tar
MKDIR=mkdir
RM=rm
LN=ln
GZIP=gzip
CP=cp
MV=mv
GREP=grep
TOUCH=touch
V=
NOOP=false
DO_COMPRESS=true
CMD_PREFIX=
SINCE_DATE="@0" # default is set to January 1, 1970 at 00:00:00 GMT
REFERENCE_FILE=/tmp/reference
BASE=bsp_dump_`hostname`_`date +%Y%m%d_%H%M%S`
DUMPDIR=/var/dump
TARDIR=$DUMPDIR/$BASE
TARFILE=$DUMPDIR/$BASE.tar
LOGDIR=$DUMPDIR/$BASE/dump
LOGROTATE_FILE=/etc/cron.daily/logrotate
BSP_UTILS_DIR=$PWD
BSP_PYTHON_DIR=$BSP_UTILS_DIR/../python
FW_TOOL_DIR=$BSP_UTILS_DIR/../../tools
BMC_TOOL_DIR=$FW_TOOL_DIR/BMC
BIOS_TOOL_DIR=$FW_TOOL_DIR/BIOS
CPLD_TOOL_DIR=$FW_TOOL_DIR/CPLD
UCD_TOOL_DIR=$FW_TOOL_DIR/UCD90120
I210_TOOL_DIR=$FW_TOOL_DIR/I210
SFP_TOOL_DIR=$FW_TOOL_DIR/SFP+
BSP_UT_FILE_PATH=$BSP_PYTHON_DIR/ut/bsp_ut.py

###############################################################################
# Runs a comamnd and saves its output to the incrementally built tar.
# Globals:
#  LOGDIR
#  BASE
#  MKDIR
#  TAR
#  TARFILE
#  DUMPDIR
#  V
#  RM
#  NOOP
# Arguments:
#  cmd: The command to run. Make sure that arguments with spaces have quotes
#  filename: the filename to save the output as in $BASE/dump
#  do_gzip: (OPTIONAL) true or false. Should the output be gzipped
# Returns:
#  None
###############################################################################
save_cmd() {
    local cmd="$1"
    local filename=$2
    local filepath="${LOGDIR}/$filename"
    local do_gzip=${3:-false}
    local tarpath="${BASE}/dump/$filename"
    [ ! -d $LOGDIR ] && $MKDIR $V -p $LOGDIR

    # eval required here to re-evaluate the $cmd properly at runtime
    # This is required if $cmd has quoted strings that should be bunched
    # as one argument, e.g. vtysh -c "COMMAND HERE" needs to have
    # "COMMAND HERE" bunched together as 1 arg to vtysh -c
    if $do_gzip
    then
        tarpath="${tarpath}.gz"
        filepath="${filepath}.gz"
        if $NOOP; then
            echo "eval $cmd 2>&1 | gzip -c > '${filepath}'"
        else
            eval "$cmd" 2>&1 | gzip -c > "${filepath}"
        fi
    else
        if $NOOP; then
            echo "eval $cmd &> '$filepath'"
        else
            eval "$cmd" &> "$filepath"
        fi
    fi
    ($TAR $V -rhf $TARFILE -C $DUMPDIR "$tarpath" \
        || abort "${ERROR_TAR_FAILED}" "tar append operation failed. Aborting to prevent data loss.") \
        && $RM $V -rf "$filepath"
}

###############################################################################
# Given list of proc files, saves proc files to tar.
# Globals:
#  V
#  TARDIR
#  MKDIR
#  CP
#  DUMPDIR
#  TAR
#  RM
#  BASE
#  TARFILE
# Arguments:
#  *procfiles: variable-length list of proc file paths to save
# Returns:
#  None
###############################################################################
save_proc() {
    local procfiles="$@"
    $MKDIR $V -p $TARDIR/proc \
        && $CP $V -r $procfiles $TARDIR/proc \
        && $TAR $V -rhf $TARFILE -C $DUMPDIR --mode=+rw $BASE/proc \
        && $RM $V -rf $TARDIR/proc
}

###############################################################################
# Runs a comamnd and saves its output to the incrementally built tar.
# Globals:
#  LOGDIR
#  BASE
#  MKDIR
#  TAR
#  TARFILE
#  DUMPDIR
#  V
#  RM
#  NOOP
# Arguments:
#  filename: the full path of the file to save
#  base_dir: the directory in $TARDIR/ to stage the file
#  do_gzip: (OPTIONAL) true or false. Should the output be gzipped
# Returns:
#  None
###############################################################################
save_file() {
    local orig_path=$1
    local supp_dir=$2
    local gz_path="$TARDIR/$supp_dir/$(basename $orig_path)"
    local tar_path="${BASE}/$supp_dir/$(basename $orig_path)"
    local do_gzip=${3:-true}
    [ ! -d "$TARDIR/$supp_dir" ] && $MKDIR $V -p "$TARDIR/$supp_dir"

    if $do_gzip; then
        gz_path="${gz_path}.gz"
        tar_path="${tar_path}.gz"
        if $NOOP; then
            echo "gzip -c $orig_path > $gz_path"
        else
            gzip -c $orig_path > $gz_path
        fi
    else
        if $NOOP; then
            echo "cp $orig_path $gz_path"
        else
            cp $orig_path $gz_path
        fi
    fi
    ($TAR $V -rhf $TARFILE -C $DUMPDIR "$tar_path" \
        || abort "${ERROR_PROCFS_SAVE_FAILED}" "tar append operation failed. Aborting to prevent data loss.") \
        && $RM $V -f "$gz_path"
}

###############################################################################
# find_files routine
# Globals:
#  SINCE_DATE: list files only newer than given date
#  REFERENCE_FILE: the file to be created as a reference to compare modification time
# Arguments:
#  directory: directory to search files in
# Returns:
#  None
###############################################################################
find_files() {
    local -r directory=$1
    $TOUCH --date="${SINCE_DATE}" "${REFERENCE_FILE}"
    local -r find_command="find -L $directory -type f -newer ${REFERENCE_FILE}"

    echo $($find_command)
}

###############################################################################
# disable_logrotate routine
# Globals:
#  None
# Arguments:
#  None
# Returns:
#  None
###############################################################################
disable_logrotate() {
    sed -i '/logrotate/s/^/#/g' ${LOGROTATE_FILE}
}

###############################################################################
# enable_logrotate routine
# Globals:
#  None
# Arguments:
#  None
# Returns:
#  None
###############################################################################
enable_logrotate() {
    sed -i '/logrotate/s/^#*//g' ${LOGROTATE_FILE}
}

###############################################################################
# Main generate_dump routine
# Globals:
#  All of them.
# Arguments:
#  None
# Returns:
#  None
###############################################################################
main() {
    if [ `whoami` != root ] && ! $NOOP;
    then
        echo "$0: must be run as root (or in sudo)" >&2
        exit 10
    fi
    ${CMD_PREFIX}renice +5 -p $$ >> /dev/null
    ${CMD_PREFIX}ionice -c 2 -n 5 -p $$ >> /dev/null

    $MKDIR $V -p $TARDIR

    # Start with this script so its obvious what code is responsible
    $LN $V -s /usr/bin/generate_dump $TARDIR
    $TAR $V -chf $TARFILE -C $DUMPDIR $BASE
    $RM $V -f $TARDIR/bsp_dump

    # Capture /proc state early
    save_proc /proc/buddyinfo /proc/cmdline /proc/consoles \
        /proc/cpuinfo /proc/devices /proc/diskstats /proc/dma \
        /proc/interrupts /proc/iomem /proc/ioports /proc/kallsyms \
        /proc/loadavg /proc/locks /proc/meminfo /proc/misc \
        /proc/modules /proc/self/mounts /proc/self/net \
        /proc/pagetypeinfo /proc/partitions /proc/sched_debug /proc/slabinfo \
        /proc/softirqs /proc/stat /proc/swaps /proc/sysvipc /proc/timer_list \
        /proc/uptime /proc/version /proc/vmallocinfo /proc/vmstat \
        /proc/zoneinfo \
        || abort "${ERROR_PROCFS_SAVE_FAILED}" "Proc saving operation failed. Aborting for safety."

    save_cmd "python3 ${BSP_UTILS_DIR}/platform_utility.py deinit " "platform-deinit"
    save_cmd "ls /usr/local/lib/python3.6/dist-packages/" "bsp-version"
    save_cmd "cd ${CPLD_TOOL_DIR}; make" "cpld-tool-make"
    save_cmd "cd ${BIOS_TOOL_DIR}; make" "bios-tool-make"
    save_cmd "cd ${BMC_TOOL_DIR}; ./upgrade_bmc.sh version" "bmc-version"
    save_cmd "cd ${CPLD_TOOL_DIR}; ./upgrade_cpld.sh version" "cpld-version"
    save_cmd "cd ${BIOS_TOOL_DIR}; ./upgrade_bios.sh version" "bios-version"
    save_cmd "cd ${BIOS_TOOL_DIR}; ./upgrade_bios.sh boot_info" "bios-boot-info"
    #save_cmd "cd ${UCD_TOOL_DIR}; ./upgrade_ucd.sh version" "ucd-version"
    save_cmd "${I210_TOOL_DIR}/eeupdate64e /NIC=3 /EEPROMVER" "i210-version"
    save_cmd "${SFP_TOOL_DIR}/eeupdate64e /NIC=1 /EEPROMVER" "sfp-version"
    save_cmd "python3 ${BSP_UTILS_DIR}/platform_utility.py init " "platform-init"
    save_cmd "cat /sys/bus/i2c/devices/0-0057/eeprom" "cpueeprom.bin"
    save_cmd "python3 ${BSP_UT_FILE_PATH} CPLD 1" "hw-version"


    save_cmd "ipmitool sensor" "ipmitool-sensor"
    save_cmd "ipmitool fru print" "ipmitool-fru-print"
    save_cmd "lspci -vvv -xx" "lspci"
    save_cmd "lsusb -v" "lsusb"
    save_cmd "i2cdetect -y 0" "i2cdetect"

    save_cmd "sysctl -a" "sysctl"

    save_cmd "ps aux" "ps.aux"
    save_cmd "free" "free"
    save_cmd "vmstat 1 5" "vmstat"
    save_cmd "vmstat -m" "vmstat.m"
    save_cmd "vmstat -s" "vmstat.s"
    save_cmd "mount" "mount"
    save_cmd "df" "df"
    save_cmd "dmesg -HP" "dmesg"

#    save_cmd "docker ps -a" "docker.ps"

    $RM $V -rf $TARDIR
    $MKDIR $V -p $TARDIR
    $MKDIR $V -p $LOGDIR
    $LN $V -s /etc $TARDIR/etc

    ($TAR $V -rhf $TARFILE -C $DUMPDIR --mode=+rw \
        --exclude="etc/alternatives" \
        --exclude="*/etc/passwd*" \
        --exclude="*/etc/shadow*" \
        --exclude="*/etc/group*" \
        --exclude="*/etc/gshadow*" \
        --exclude="*/etc/ssh*" \
        --exclude="*get_creds*" \
        --exclude="*snmpd.conf*" \
        --exclude="/etc/mlnx" \
        --exclude="/etc/mft" \
        $BASE/etc \
        || abort "${ERROR_TAR_FAILED}" "Tar append operation failed. Aborting for safety.") \
        && $RM $V -rf $TARDIR

    disable_logrotate
    trap enable_logrotate HUP INT QUIT TERM KILL ABRT ALRM

    # gzip up all log files individually before placing them in the incremental tarball
    for file in $(find_files "/var/log/"); do
        # ignore the sparse file lastlog
        if [ "$file" = "/var/log/lastlog" ]; then
            continue
        fi
        # don't gzip already-gzipped log files :)
        if [ -z "${file##*.gz}" ]; then
            save_file $file log false
        else
            save_file $file log true
        fi
    done

    enable_logrotate

    # archive core dump files
    for file in $(find_files "/var/core/"); do
        # don't gzip already-gzipped log files :)
        if [ -z "${file##*.gz}" ]; then
            save_file $file core false
        else
            save_file $file core true
        fi
    done

    # archive crash dump files
    for file in $(find_files "/var/crash/"); do
        # don't gzip already-gzipped log files :)
        if [ -z "${file##*.gz}" ]; then
            save_file $file core false
        else
            save_file $file core true
        fi
    done

    # archive systemd crash dump files
    for file in $(find_files "/var/lib/systemd/coredump/"); do
        # don't gzip already-gzipped log files :)
        if [ -z "${file##*.gz}" ]; then
            save_file $file core false
        else
            save_file $file core true
        fi
    done

    # clean up working tar dir before compressing
    $RM $V -rf $TARDIR

    if $DO_COMPRESS; then
        $GZIP $V $TARFILE
        if [ $? -eq 0 ]; then
            TARFILE="${TARFILE}.gz"
        else
            echo "WARNING: gzip operation appears to have failed." >&2
        fi
    fi

    echo ${TARFILE}
}

###############################################################################
# Terminates generate_dump early just in case we have issues.
# Globals:
#  None
# Arguments:
#  retcode: 0-255 return code to exit with. default is 1
#  msg: (OPTIONAL) msg to print to standard error
# Returns:
#  None
###############################################################################
abort() {
    local exitcode=${1:-1}
    local msg=${2:-Error. Terminating early for safety.}
    echo "$msg" >&2
    exit $exitcode
}

###############################################################################
# Prints usage to stdout.
# Globals:
#  None
# Arguments:
#  None
# Returns:
#  None
###############################################################################
usage() {
    cat <<EOF
$0 [-xnvh]

Create a system dump for support/debugging. Requires root privileges.

OPTIONS
    -x
        Enable bash debug mode.
    -h
        The usage information you are reading right now
    -v
        Enable verbose mode. All commands (like tar, mkdir, rm..) will have -v
        passed to them
    -n
        Noop mode. Don't actually create anything, just echo what would happen
    -z
        Don't compress the tar at the end.
    -s DATE
        Collect logs since DATE;
        The argument is a mostly free format human readable string such as
        "24 March", "yesterday", etc.

EOF
}

while getopts ":xnvhzs:" opt; do
    case $opt in
        x)
            # enable bash debugging
            PS4="+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }"
            set -x
            ;;
        h)
            usage
            exit 0
            ;;
        v)
            # echo commands about to be run to stderr
            set -v
            V="-v"
            ;;
        n)
            TAR="echo tar"
            MKDIR="echo mkdir"
            RM="echo rm"
            LN="echo ln"
            GZIP="echo gzip"
            CMD_PREFIX="echo "
            MV="echo mv"
            CP="echo cp"
            TOUCH="echo touch"
            NOOP=true
            ;;
        z)
            DO_COMPRESS=false
            ;;
        s)
            SINCE_DATE="${OPTARG}"
            # validate date expression
            date --date="${SINCE_DATE}" &> /dev/null || abort "${ERROR_INVALID_ARGUMENT}" "Invalid date expression passed: '${SINCE_DATE}'"
            ;;
        /?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

main
