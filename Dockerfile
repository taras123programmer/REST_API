FROM python:3.10-slim-buster

WORKDIR /flask_app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD flask db upgrade && flask run --host=0.0.0.0 --port=5000
