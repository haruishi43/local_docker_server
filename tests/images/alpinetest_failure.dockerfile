FROM alpine:latest
LABEL maintainer="Haruya Ishikawa <haru.ishi43@gmail.com"

RUN apk --update add --no-cache openssh bash \
    && rm -rf /var/cache/apk/*

# NOTE: should raise error while building
COPY doesnt_exist.txt .

EXPOSE 22
