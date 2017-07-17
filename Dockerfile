# Copyright (c) Nicholas Lourie
#
# This Dockerfile is used in developing [the runcli project][1].
#
# [1]: https://github.com/nalourie/runcli


FROM debian:stable


# add system packages, i.e. pip and python3
RUN apt-get clean \
 && apt-get update --fix-missing \
 && apt-get install -y \
      python-pip \
      python3 \
      python3-pip

# pull in the code base from the context
ADD . /root/runcli

RUN pip install -e /root/runcli
