FROM python:3.8.8
LABEL description="ag-isbnapi-fastapi" type="dev"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends vim wget apt-utils

RUN wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py && \
    python get-poetry.py --yes && \
    rm get-poetry.py
ENV PATH="/root/.poetry/bin:${PATH}"
RUN poetry config virtualenvs.create false

COPY /pyproject.toml ./poetry.lock /utils/
WORKDIR /utils/
RUN poetry install

EXPOSE 8000
COPY . /project
WORKDIR /project
ENTRYPOINT uvicorn main:app --reload
