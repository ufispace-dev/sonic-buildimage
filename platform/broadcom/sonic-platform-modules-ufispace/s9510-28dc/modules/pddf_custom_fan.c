#include <linux/module.h>
#include <linux/jiffies.h>
#include <linux/i2c.h>
#include <linux/hwmon.h>
#include <linux/hwmon-sysfs.h>
#include <linux/err.h>
#include <linux/delay.h>
#include <linux/mutex.h>
#include <linux/sysfs.h>
#include <linux/slab.h>
#include <linux/dmi.h>
#include <linux/io.h>
#include "../../../../pddf/i2c/modules/include/pddf_fan_defs.h"
#include "../../../../pddf/i2c/modules/include/pddf_fan_driver.h"

extern int board_i2c_cpld_read_custom(unsigned short cpld_addr, u8 reg);
extern FAN_SYSFS_ATTR_DATA data_fan1_present;
extern FAN_SYSFS_ATTR_DATA data_fan2_present;
extern FAN_SYSFS_ATTR_DATA data_fan3_present;
extern FAN_SYSFS_ATTR_DATA data_fan4_present;
extern FAN_SYSFS_ATTR_DATA data_fan5_present;

int sonic_i2c_get_fan_present_custom(void *client, FAN_DATA_ATTR *udata, void *info);

int sonic_i2c_get_fan_present_custom(void *client, FAN_DATA_ATTR *udata, void *info)
{
    int status = 0;
    int val = 0;
    struct fan_attr_info *painfo = (struct fan_attr_info *)info;

    if (strcmp(udata->devtype, "cpld") == 0)
    {
        if (udata!=NULL)
        {
            val = board_i2c_cpld_read_custom(udata->devaddr , udata->offset);
        } else {
            val = -1;
        }
    } else {
        val = -1;
    }
	
	if (val < 0)
		status = val;
	else
		painfo->val.intval = ((val & udata->mask) == udata->cmpval);
    

    return status;
}

static int __init pddf_custom_fan_init(void)
{
  data_fan1_present.do_get = sonic_i2c_get_fan_present_custom;
  data_fan2_present.do_get = sonic_i2c_get_fan_present_custom;
  data_fan3_present.do_get = sonic_i2c_get_fan_present_custom;
  data_fan4_present.do_get = sonic_i2c_get_fan_present_custom;
  data_fan5_present.do_get = sonic_i2c_get_fan_present_custom;
  return 0;
}

static void __exit pddf_custom_fan_exit(void)
{
  return;
}

MODULE_AUTHOR("Nonodark Huang <nonodark.huang@ufispace.com>");
MODULE_DESCRIPTION("pddf custom fan api");
MODULE_LICENSE("GPL");

module_init(pddf_custom_fan_init);
module_exit(pddf_custom_fan_exit);

