
MODULE_NAME  = x86-64-ufispace-s6301-56stp-sys-eeprom.o x86-64-ufispace-s6301-56stp-lpc.o pddf_custom_psu.o
obj-m       := $(MODULE_NAME)
x86-64-ufispace-s6301-56stp-poe-objs := x86-64-ufispace-s6301-56stp-poe-module.o x86-64-ufispace-s6301-56stp-poe-hal.o x86-64-ufispace-s6301-56stp-poe-api.o
obj-m       += x86-64-ufispace-s6301-56stp-poe.o

CFLAGS_pddf_custom_sysstatus_module.o := -I$(M)/../../../../pddf/i2c/modules/include
KBUILD_EXTRA_SYMBOLS := $(M)/../../../../pddf/i2c/Module.symvers.PDDF
