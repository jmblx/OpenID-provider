#!/bin/sh
alembic upgrade head

make server-prod
