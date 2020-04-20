REV := $(shell git rev-parse --short HEAD)
NAME = tickets

.PHONY: prod dev build build-dev

prod: build
dev: build-dev

build:
	@echo ${REV}
	docker build . --target runner --tag "${NAME}:${REV}"

build-dev:
	docker build . --target dev --tag "${NAME}:${REV}-dev"
