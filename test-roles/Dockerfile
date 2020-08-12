FROM python:3.7.8-buster

RUN mkdir /src
WORKDIR /src

ADD requirements.txt /src
RUN pip install -r requirements.txt

ADD test_roles.py /src

ENTRYPOINT ["python", "test_roles.py"]
