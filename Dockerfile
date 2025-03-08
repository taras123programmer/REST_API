FROM python:3.10-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
