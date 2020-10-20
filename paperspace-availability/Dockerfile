FROM python:3.8.6-alpine3.12

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install -e .

ENTRYPOINT ["python", "main.py"]

