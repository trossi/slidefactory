SIF=slidefactory.sif

build: $(SIF)

clean:
	rm $(SIF)

%.sif: %.tar
	rm -f $@
	singularity build $@ docker-archive://$<

slidefactory.tar: Dockerfile pandoc convert.sh
	podman build --format docker \
		-t $(@:.tar=:test) \
		.
	rm -f $@
	podman save $(@:.tar=:test) -o $@


pandoc:
	wget https://github.com/jgm/pandoc/releases/download/3.1.2/pandoc-3.1.2-linux-amd64.tar.gz -O - | tar -xvzf - pandoc-3.1.2/bin/pandoc --strip-components=2
