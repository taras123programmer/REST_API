#!/bin/bash

sudo docker build -t flask-rest-api_2 . && 

sudo docker run -d -p 5000:5000 flask-rest-api_2
