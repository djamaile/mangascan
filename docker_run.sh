#!/usr/bin/env bash

docker build -t mangascan .
docker run -p 5000:5000 mangascan