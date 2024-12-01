#!/bin/sh

cd /fastapi-app

make migration

make server-prod
