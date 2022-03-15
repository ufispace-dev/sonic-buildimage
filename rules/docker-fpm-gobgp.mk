# docker image for fpm-gobgp

DOCKER_FPM_GOBGP = docker-fpm-gobgp.gz
$(DOCKER_FPM_GOBGP)_PATH = $(DOCKERS_PATH)/docker-fpm-gobgp
$(DOCKER_FPM_GOBGP)_DEPENDS += $(GOBGP)
$(DOCKER_FPM_GOBGP)_LOAD_DOCKERS += $(DOCKER_FPM_QUAGGA)
SONIC_DOCKER_IMAGES += $(DOCKER_FPM_GOBGP)

$(DOCKER_FPM_GOBGP)_CONTAINER_NAME = bgp
$(DOCKER_FPM_GOBGP)_RUN_OPT += --privileged -t
$(DOCKER_FPM_GOBGP)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
$(DOCKER_FPM_GOBPG)_FILES += $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)