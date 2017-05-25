FROM pypy:2
MAINTAINER Cory Benfield <lukasaoz@gmail.com>

RUN echo deb http://httpredir.debian.org/debian jessie-backports main >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y -t jessie-backports libssl-dev
RUN pip install -U setuptools
RUN pip install -U pip

RUN mkdir /certs
ADD src /python/src
ADD setup.py /python/setup.py
ADD requirements.txt requirements.txt

RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["pip", "install", "/python"]

CMD ["twist", "certifiproxy"]
