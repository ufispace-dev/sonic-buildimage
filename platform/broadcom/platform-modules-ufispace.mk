# UfiSpace S9700_53DX Platform modules

UFISPACE_S9700_53DX_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S9300_32D_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S9301_32D_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S9110_32X_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S8901_54XC_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S6301_56ST_PLATFORM_MODULE_VERSION = 1.0.0

export UFISPACE_S9700_53DX_PLATFORM_MODULE_VERSION
export UFISPACE_S9300_32D_PLATFORM_MODULE_VERSION
export UFISPACE_S9301_32D_PLATFORM_MODULE_VERSION
export UFISPACE_S9110_32X_PLATFORM_MODULE_VERSION
export UFISPACE_S8901_54XC_PLATFORM_MODULE_VERSION
export UFISPACE_S6301_56ST_PLATFORM_MODULE_VERSION

UFISPACE_S9700_53DX_PLATFORM_MODULE = sonic-platform-ufispace-s9700-53dx_$(UFISPACE_S9700_53DX_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-ufispace
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s9700_53dx-r0
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r1
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r2
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r3
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r4
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r5
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r6
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r7
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r8
$(UFISPACE_S9700_53DX_PLATFORM_MODULE)_PLATFORM += x86_64-ufispace_s9700_53dx-r9
SONIC_DPKG_DEBS += $(UFISPACE_S9700_53DX_PLATFORM_MODULE)


UFISPACE_S9300_32D_PLATFORM_MODULE = sonic-platform-ufispace-s9300-32d_$(UFISPACE_S9300_32D_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S9300_32D_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s9300_32d-r0
$(eval $(call add_extra_package,$(UFISPACE_S9700_53DX_PLATFORM_MODULE),$(UFISPACE_S9300_32D_PLATFORM_MODULE)))

UFISPACE_S9301_32D_PLATFORM_MODULE = sonic-platform-ufispace-s9301-32d_$(UFISPACE_S9301_32D_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S9301_32D_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s9301_32d-r0
$(eval $(call add_extra_package,$(UFISPACE_S9700_53DX_PLATFORM_MODULE),$(UFISPACE_S9301_32D_PLATFORM_MODULE)))

UFISPACE_S9110_32X_PLATFORM_MODULE = sonic-platform-ufispace-s9110-32x_$(UFISPACE_S9110_32X_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S9110_32X_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s9110_32x-r0
$(eval $(call add_extra_package,$(UFISPACE_S9700_53DX_PLATFORM_MODULE),$(UFISPACE_S9110_32X_PLATFORM_MODULE)))

UFISPACE_S8901_54XC_PLATFORM_MODULE = sonic-platform-ufispace-s8901-54xc_$(UFISPACE_S8901_54XC_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S8901_54XC_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s8901_54xc-r0
$(eval $(call add_extra_package,$(UFISPACE_S9700_53DX_PLATFORM_MODULE),$(UFISPACE_S8901_54XC_PLATFORM_MODULE)))

UFISPACE_S6301_56ST_PLATFORM_MODULE = sonic-platform-ufispace-s6301-56st_$(UFISPACE_S6301_56ST_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S6301_56ST_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s6301_56st-r0
$(eval $(call add_extra_package,$(UFISPACE_S9700_53DX_PLATFORM_MODULE),$(UFISPACE_S6301_56ST_PLATFORM_MODULE)))
