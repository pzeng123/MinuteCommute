#Dockerfile

FROM ubuntu:16.04

MAINTAINER Peng "peng8296@gmail.com"

RUN apt-get update && \
    apt-get install -y \
    python python-dev python-pip
RUN pip install --upgrade pip

RUN mkdir -p /var/www/demo
ADD views.py /var/www/demo/views.py
ADD wsgi.py /var/www/demo/wsgi.py
ADD myproject /etc/nginx/sites-available/
ADD start.sh /var/www/demo/start.sh


# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /var/www/demo/requirements.txt

WORKDIR /var/www/demo

RUN pip install -r requirements.txt


COPY . /var/www/demo
EXPOSE 80
EXPOSE 8000

RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled

CMD ["sh", "start.sh"]
