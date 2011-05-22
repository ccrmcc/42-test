#!/bin/sh

set -e

fname=$(date +%Y_%m_%d).dat
env PYTHONPATH=. python dj42cc_test/manage.py modelscount 2> $fname
