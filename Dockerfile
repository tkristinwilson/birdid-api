# Docker Layers: RUN, COPY, ADD create layers

# https://hub.docker.com/_/python/
FROM python:3.7.5-slim-buster

# resynchronize the package index files from their sources
# -y is 'automatic yes'
# RUN apt-get update # prevents your Dockerfile from creating consistent, immutable builds.
# python3 and GNU C compiler
# RUN apt-get install -y python3-dev gcc
# 
# RUN apt-get update && apt-get install -y python3-dev gcc build-essential
RUN apt-get update && apt-get install --no-install-recommends --yes python3-dev gcc

# Layer caching, skip installing python reqs if the file doesn't change
WORKDIR /home/app

COPY requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt 
# Dependency of Fastai (PEP 517 error workaround)
RUN pip install --no-cache-dir Bottleneck==1.3.1
RUN pip install --no-cache-dir torch==1.3.1 torchvision==0.4.2 fastai==1.0.59

# Resnet34
ADD https://download.pytorch.org/models/resnet34-333f7ec4.pth /root/.cache/torch/checkpoints/resnet34-333f7ec4.pth

# Copy application files
COPY src/ /home/app/

EXPOSE 5000

# https://pythonspeed.com/articles/gunicorn-in-docker/
# change default directory for the heartbeat file
# docker run --rm -it ubuntu:18.04 df
# gunicorn --worker-tmp-dir /dev/shm ...
# start at least two workers
# gunicorn --workers=2 --threads=4 --worker-class=gthread
# Container schedulers typically expect logs to come out on stdout/stderr, so you should configure Gunicorn to do so:
# gunicorn --log-file=- 
CMD ["gunicorn", "--workers", "4", "--worker-tmp-dir", "/home/app",  "--bind", "0.0.0.0:5000", "app:app"]