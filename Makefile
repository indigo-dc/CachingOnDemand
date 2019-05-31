RELEASE = helm
CHART_NAME = cachingondemand
GH_PAGES = https://cloud-pg.github.io/CachingOnDemand/
COMMIT_MSG = "update helm"

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

helm-build:
	helm package ${RELEASE}/${CHART_NAME}
	helm repo index ./ --url ${GH_PAGES}
	mv ./index.yaml /tmp/
	mv ./${CHART_NAME}*.tgz /tmp/
	git checkout gh-pages
	cp /tmp/${CHART_NAME}*.tgz .
	cp /tmp/index.yaml .
	git add index.yaml *.tgz
	git commit -m ${COMMIT_MSG}
	git push origin gh-pages
	git checkout ${CURRENT_BRANCH}