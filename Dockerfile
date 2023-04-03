FROM docker.io/astefanutti/decktape:3.7.0

LABEL org.opencontainers.image.source=https://github.com/trossi/slidefactory

USER root

RUN apk update && \
    apk add --no-cache \
      font-noto \
      font-inconsolata \
      && \
    rm -rf /var/cache/apk/*

ADD pandoc /usr/local/bin/

ENV SLIDEFACTORY_ROOT=/slidefactory

ENV SLIDEFACTORY_THEME_ROOT=$SLIDEFACTORY_ROOT/theme \
    PATH=$SLIDEFACTORY_ROOT/bin:$PATH

ADD theme/ $SLIDEFACTORY_THEME_ROOT/
ADD convert.sh $SLIDEFACTORY_ROOT/bin/

RUN mkdir /work

WORKDIR /work

ENTRYPOINT ["convert.sh"]
CMD ["-h"]
