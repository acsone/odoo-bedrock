ifndef ODOOVERSION
$(error ODOOVERSION is not set)
endif

ifndef PYTHONTAG
$(error PYTHONTAG is not set)
endif

ifndef PYTHONBIN
$(error PYTHONBIN is not set)
endif

ifndef TAG
TAG=latest
endif

ifndef REGISTRY
$(error REGISTRY is not set)
endif

BASENAME=odoo-bedrock
NAME=$(REGISTRY)/acsone/$(BASENAME)
IMAGE=$(NAME):$(ODOOVERSION)-$(PYTHONTAG)

export

all: build


.PHONY: build
build:
	docker build --no-cache --build-arg PYTHONBIN=$(PYTHONBIN) -f ./Dockerfile-$(ODOOVERSION) -t $(IMAGE) .


.PHONY: tag
tag:
	docker tag $(IMAGE) $(IMAGE)-$(TAG)


.PHONY: push
push:
	docker push $(IMAGE)-$(TAG)


.PHONY: test
test:
	bash test.sh
