FROM quay.io/keboola/docker-custom-python:latest

COPY . /code/
WORKDIR /data/out/tables/

RUN pip install requests
RUN pip install xmltodict

CMD ["python", "-u", "/code/main.py"]
