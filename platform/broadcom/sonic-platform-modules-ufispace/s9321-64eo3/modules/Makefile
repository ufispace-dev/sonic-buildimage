
x86-64-ufispace-s9321-64eo3-cpld-objs := x86-64-ufispace-s9321-64eo3-cpld-main.o x86-64-ufispace-s9321-64eo3-cpld-mux.o
MODULE_NAME  = x86-64-ufispace-s9321-64eo3-cpld.o x86-64-ufispace-s9321-64eo3-sys-eeprom.o x86-64-ufispace-s9321-64eo3-lpc.o pddf_custom_sysstatus_module.o pddf_custom_cpldmux_driver.o x86-64-ufispace-s9321-64eo3-i2c-smbus.o
obj-m       := $(MODULE_NAME)

CFLAGS_pddf_custom_sysstatus_module.o := -I$(M)/../../../../pddf/i2c/modules/include
CFLAGS_pddf_custom_cpldmux_driver.o := -I$(M)/../../../../pddf/i2c/modules/include
KBUILD_EXTRA_SYMBOLS := $(KERNEL_SRC)/Module.symvers.PDDF
