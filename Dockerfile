# syntax=docker/dockerfile:1
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install git pipx
RUN pipx install poetry
COPY ./ebu_tt_live ./testing ./pyproject.toml ./poetry.lock ./
RUN /root/.local/bin/poetry install
CMD poetry run ebu-dummy-encoder
