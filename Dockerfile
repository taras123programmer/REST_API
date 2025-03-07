FROM python3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip intall --upgrade pip && pip install -r -requirements.txt

COPY . .

EXPOSE 5050

ENTRYPOINT ["python", "run:app", "--host", "0.0.0.0", "-port", "5050"]