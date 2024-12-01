#!/bin/sh

cd /fastapi_app

make migration

make server-prod
