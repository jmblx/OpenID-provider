#!/bin/sh
cd src

make migration

make server-prod
