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
#include "../../../../pddf/i2c/modules/include/pddf_psu_defs.h"
#include "../../../../pddf/i2c/modules/include/pddf_psu_driver.h"

/*#define PSU_DEBUG*/
#ifdef PSU_DEBUG
#define psu_dbg(...) printk(__VA_ARGS__)
#else
#define psu_dbg(...)
#endif

extern int board_i2c_cpld_read_custom(unsigned short cpld_addr, u8 reg);
extern PSU_SYSFS_ATTR_DATA access_psu_present;
extern PSU_SYSFS_ATTR_DATA access_psu_power_good;

int sonic_i2c_get_psu_byte_custom(void *client, PSU_DATA_ATTR *adata, void *data)
{
    int status = 0;
    int val = 0;
    struct psu_attr_info *padata = (struct psu_attr_info *)data;


    if (strncmp(adata->devtype, "cpld", strlen("cpld")) == 0)
    {
        val = board_i2c_cpld_read_custom(adata->devaddr , adata->offset);
        if (val < 0)
            return val;
        padata->val.intval =  ((val & adata->mask) == adata->cmpval);
        psu_dbg(KERN_ERR "%s: byte_value = 0x%x\n", __FUNCTION__, padata->val.intval);
    }

    return status;
}

static int __init pddf_custom_psu_init(void)
{
  access_psu_present.do_get = sonic_i2c_get_psu_byte_custom;
  access_psu_power_good.do_get = sonic_i2c_get_psu_byte_custom;
  return 0;
}

static void __exit pddf_custom_psu_exit(void)
{
  return;
}

MODULE_AUTHOR("Nonodark Huang <nonodark.huang@ufispace.com>");
MODULE_DESCRIPTION("pddf custom psu api");
MODULE_LICENSE("GPL");

module_init(pddf_custom_psu_init);
module_exit(pddf_custom_psu_exit);

