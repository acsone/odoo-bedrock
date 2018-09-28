BASENAME=odoo-bedrock
NAME=acsone/$(BASENAME)

ifndef VERSION
$(error VERSION is not set)
endif

IMAGE=$(NAME):$(VERSION)
IMAGE_LATEST=$(IMAGE)-latest

export

all: build


.PHONY: build
build:
	docker build --no-cache -f ./Dockerfile-$(VERSION) -t $(IMAGE_LATEST) .


.PHONY: tag
tag:
	docker tag $(IMAGE_LATEST) $(IMAGE)-$(TAG)


.PHONY: push
push:
	docker push $(IMAGE)-$(TAG)


.PHONY: test
test:
	bash test.sh
