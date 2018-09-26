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


.PHONY: tag_latest_main
tag_latest_main:
	docker tag $(IMAGE_LATEST) $(NAME):latest


.PHONY: push_latest_main
push_latest_main:
	docker push $(NAME):latest


.PHONY: test
test:
	bash test.sh
