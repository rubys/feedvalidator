#!/bin/sh

PYTHON=${1:-${PYTHON:-python}}

# Run all project tests

cd "`dirname "$0"`"

${PYTHON} validtest.py

${PYTHON} messagetest.py

# Make sure XML encoding detection works
${PYTHON} tests/genXmlTestcases.py && python tests/testXmlEncoding.py

# Confirm that XML is decoded correctly
${PYTHON} tests/testXmlEncodingDecode.py

# Make sure media type checks are consistent
${PYTHON} tests/testMediaTypes.py
