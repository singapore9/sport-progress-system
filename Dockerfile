# docker build -t testcontainer .
# docker run -p 8000:8000 -it testcontainer /bin/sh
FROM python:3.9.12-bullseye
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

RUN mkdir project
COPY pyproject.toml project/
COPY poetry.lock project/
WORKDIR ./project

RUN poetry config virtualenvs.in-project true
RUN poetry install

COPY . .

EXPOSE 8000
