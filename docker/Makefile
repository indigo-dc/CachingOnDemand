VERSION ?= `git describe --tags`

NS ?= cloudpg
IMAGE_NAME ?= cachingondemand
CONTAINER_NAME ?= cachingondemand
CONTAINER_INSTANCE ?= default


.PHONY: build compile-plugins build-no-plugin push shell run start stop rm release login

all: help

help:
	@echo "Available commands:\n"
	@echo "- build			: "
	@echo "- build-doc		:"
	@echo "- compile-plugins	: "
	@echo "- build-no-plugin	: "
	@echo "- push			: "
	@echo "- shell			: "
	@echo "- run			: "
	@echo "- start			: "
	@echo "- stop			: "
	@echo "- rm			: "
	@echo "- release		: "
	@echo "- login			: "
	@echo "- compose-up		: "
	@echo "- compose-down		: "


build: Dockerfile
	docker build --target plugin_server -t $(NS)/$(IMAGE_NAME):$(VERSION) -f Dockerfile .

build-doc:
	pip install mkdocs mkdocs-material

compile-plugins: Dockerfile
	docker build --target plugins -t $(NS)/$(IMAGE_NAME):plugins -f Dockerfile .

build-no-plugin: Dockerfile
	docker build --target server -t $(NS)/$(IMAGE_NAME):$(VERSION)-noplug -f Dockerfile .

push: login
	docker push $(NS)/$(IMAGE_NAME):$(VERSION)

shell:
	docker exec -ti $(CONTAINER_NAME)-$(CONTAINER_INSTANCE) /bin/bash

run:
	docker run --rm -ti --entrypoint /bin/bash --name $(CONTAINER_NAME)-$(CONTAINER_INSTANCE) $(NS)/$(IMAGE_NAME):$(VERSION)

start:
	docker run -d --name $(CONTAINER_NAME)-$(CONTAINER_INSTANCE) $(NS)/$(IMAGE_NAME):$(VERSION)

stop:
	docker stop $(CONTAINER_NAME)-$(CONTAINER_INSTANCE)

rm:
	docker rm $(CONTAINER_NAME)-$(CONTAINER_INSTANCE)

release: login build
	make push -e VERSION=$(VERSION)

login:
	docker login

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down
