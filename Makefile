SIF=slidefactory.sif
IMAGE=slidefactory
TAG=0.1.0

build: Dockerfile pandoc convert.sh
	podman build --format docker \
		-t ${IMAGE_ROOT}/${IMAGE}:${TAG} \
		.

push:
	podman push ${IMAGE_ROOT}/${IMAGE}:${TAG}

singularity:
	rm -f $(SIF) $(SIF:.sif=.tar)
	podman save ${IMAGE_ROOT}/${IMAGE}:${TAG} -o $(SIF:.sif=.tar)
	singularity build $(SIF) docker-archive://$(SIF:.sif=.tar)
	rm -f $(SIF:.sif=.tar)

clean:
	rm $(SIF)
	rm pandoc

pandoc:
	wget https://github.com/jgm/pandoc/releases/download/3.1.2/pandoc-3.1.2-linux-amd64.tar.gz -O - | tar -xvzf - pandoc-3.1.2/bin/pandoc --strip-components=2
