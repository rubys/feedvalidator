#!/bin/sh

# Run all project tests

cd "`dirname "$0"`"

python validtest.py

python messagetest.py

python tests/genXmlTestcases.py && python tests/testXmlEncoding.py
