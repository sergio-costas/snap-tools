#!/bin/sh

set -e

test_style () {
    echo Checking $1 with Pylint...
    pylint $1
    echo Checking $1 with Flake8...
    flake8 --max-line-length=120 $1
    echo
}

test_style remove_common.py
test_style unittests.py
