.PHONY: help \
		build \
		compile-plugins \
		build-no-plugin \
		push \
		shell \
		run \
		start \
		stop \
		rm \
		release \
		login \
		compose-up \
		compose-down

all: help

help build compile-plugins build-no-plugin push shell run start stop rm release login:
	$(MAKE) -C docker $@

compose-up compose-down:
	$(MAKE) -C docker $@

