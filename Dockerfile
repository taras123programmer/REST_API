### flask_rest_api_1

# FROM python:3.10-slim-buster

# WORKDIR /app

# COPY requirements.txt requirements.txt

# RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# COPY . .

# EXPOSE 5000

# ENTRYPOINT ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]



### flask_rest_api_2

# --- Stage 1: Build dependencies ---
FROM python:3.10-slim-buster as builder

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# --- Stage 2: Final runtime image ---
FROM python:3.10-slim-buster

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]


