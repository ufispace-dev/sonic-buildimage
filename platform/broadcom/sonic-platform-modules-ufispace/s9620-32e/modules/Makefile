
x86-64-ufispace-s9620-32e-cpld-objs := x86-64-ufispace-s9620-32e-cpld-main.o x86-64-ufispace-s9620-32e-cpld-mux.o
MODULE_NAME  = x86-64-ufispace-s9620-32e-cpld.o x86-64-ufispace-s9620-32e-sys-eeprom.o x86-64-ufispace-s9620-32e-lpc.o pddf_custom_sysstatus_module.o 
obj-m       := $(MODULE_NAME)

CFLAGS_pddf_custom_sysstatus_module.o := -I$(M)/../../../../pddf/i2c/modules/include
KBUILD_EXTRA_SYMBOLS := $(M)/../../../../pddf/i2c/Module.symvers.PDDF
