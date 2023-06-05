#!/bin/bash

cd ..
docker build -t text2image-bot:latest .
docker run --env-file=.env -it text2image-bot:latest