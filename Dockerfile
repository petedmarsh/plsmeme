FROM python:3.7-buster

RUN apt update && apt install catimg

WORKDIR /plsmeme

COPY requirements.txt /plsmeme/

RUN pip install -r requirements.txt

COPY . /plsmeme
COPY plsmeme.toml /plsmeme/config/default.toml

RUN pip install -e .

ENTRYPOINT ["python", "/plsmeme/plsmeme/main.py"]
