
MODULE_NAME  = x86-64-ufispace-s9510-28dc-eeprom-mb.o x86-64-ufispace-s9510-28dc-lpc.o pddf_custom_cpld_driver.o pddf_custom_psu.o  pddf_custom_fan.o pddf_custom_led_module.o pddf_custom_sysstatus_module.o
obj-m       := $(MODULE_NAME)

CFLAGS_pddf_custom_sysstatus_module.o := -I$(M)/../../../../pddf/i2c/modules/include
KBUILD_EXTRA_SYMBOLS := $(M)/../../../../pddf/i2c/Module.symvers.PDDF
