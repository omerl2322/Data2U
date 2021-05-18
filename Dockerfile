FROM artifactory.outbrain.com:5005/baseimages/python-base-miniconda3-4712:latest

ARG SERVICE_NAME=push_report_service
ENV SERVICE_NAME=$SERVICE_NAME

RUN apt-get update && \
    apt-get install -y vim nano default-libmysqlclient-dev python-pip python-dev

COPY environment_docker.yaml /environment_docker.yml
RUN set -ex && \
    conda env create -f /environment_docker.yml
RUN conda init
RUN echo "conda activate push_report_service_env" >> ~/.bashrc
ENV BASH_ENV ~/.bashrc

EXPOSE 8000
COPY . /outbrain/Prod/Apps/push_report_sys/
WORKDIR /outbrain/Prod/Apps/push_report_sys/

# starting gunicorn
#CMD ["gunicorn", "-c", "python:gunicorn_conf", "app.report_service:app"]

# starts the services
ENTRYPOINT ["./entrypoint.sh"]

