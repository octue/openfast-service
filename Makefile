AUTHOR=danielkelshaw
REPO=xfoil
IMAGE=$(AUTHOR)/$(REPO)

default: build

build: Dockerfile
	@docker build -t $(IMAGE) .

run:
	@docker run -ti --rm --name xfoil $(IMAGE)

stop:
	@docker stop xfoil

