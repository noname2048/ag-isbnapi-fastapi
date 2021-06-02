FROM python:3.8.8
LABEL description="ag-isbnapi-fastapi" type="dev"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends vim wget apt-utils

# install poetry
RUN wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py && \
    python get-poetry.py --yes && \
    rm get-poetry.py
ENV PATH="/root/.poetry/bin:${PATH}"
RUN poetry config virtualenvs.create false

# poetry install
COPY /pyproject.toml ./poetry.lock /utils/
WORKDIR /utils/
RUN poetry install

# dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz &&\
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz &&\
    rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# server
EXPOSE 8000
COPY . /project
WORKDIR /project
CMD /bin/bash
