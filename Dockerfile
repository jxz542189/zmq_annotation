FROM ubuntu:16.04
MAINTAINER jxz
RUN rm /etc/apt/sources.list
COPY sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y apt-transport-https vim iproute2 net-tools build-essential ca-certificates curl wget software-properties-common
RUN apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl wget software-properties-common
#RUN apt-get install python3 python-dev python3-dev \
#     build-essential libssl-dev libffi-dev \
#     libxml2-dev libxslt1-dev zlib1g-dev \
#     python-pip
#安装python3.6 来自第三方
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y python3.6
RUN apt install -y python3.6-dev
RUN apt install -y python3.6-venv
#为3.6安装pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
RUN ln -s /usr/bin/python3.6 /usr/bin/python
ENV PYTHONIOENCODING=utf-8
#RUN pip install -r requirements.txt
#RUN apt-get install libssl-dev libffi-dev \
#     libxml2-dev libxslt1-dev zlib1g-dev
#RUN apt-get install python3 python-dev python3-dev \
#     build-essential libssl-dev libffi-dev \
#     libxml2-dev libxslt1-dev zlib1g-dev \
#     python-pip
COPY ./ /app
COPY ./Docker/entrypoint.sh /app
WORKDIR /app
RUN cd /app
RUN pip install -r requirements.txt
#ENTRYPOINT ["/app/entrypoint.sh"]
#CMD []
