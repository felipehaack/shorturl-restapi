#!/bin/bash

FROM ubuntu:14.04

#Ubuntu packages
RUN rm -f /etc/localtime
RUN ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git supervisor python-dev python-pip nginx python3-dev libxml2-dev libxslt1-dev libgeos-dev libncurses5-dev gettext postgresql-server-dev-all

#GitHub
RUN mkdir -p /root/.ssh
ADD id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
CMD ["echo" , "Host bitbucket.org\n\tStrictHostKeyChecking no\n" , ">>" , "/root/.ssh/config"]

#Project
RUN git clone git@bitbucket.org:felipehaack/chaordic-restapi.git --progress --verbose
RUN cd chaordic-restapi; pip install -r requirements.txt
RUN mkdir -p /chaordic-restapi/static_files
RUN mkdir -p /chaordic-restapi/logs

RUN touch /chaordic-restapi/logs/supervisor.err.log
RUN touch /chaordic-restapi/logs/supervisor.out.log

ADD gunicorn /chaordic-restapi/gunicorn
RUN chmod u+x /chaordic-restapi/gunicorn

RUN ["python", "/chaordic-restapi/manage.py", "migrate"]

ADD . /opt/django/

#Nginx
#RUN echo "daemon off;" >> /etc/nginx/nginx.conf
#RUN rm /etc/nginx/sites-enabled/default
#RUN ln -s /opt/django/django.conf /etc/nginx/sites-enabled/
RUN ln -s /opt/django/supervisord.conf /etc/supervisor/conf.d/

EXPOSE 8000

CMD ["supervisord"]
