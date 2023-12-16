FROM ubuntu:latest
LABEL authors="mahshid"

ENTRYPOINT ["top", "-b"]