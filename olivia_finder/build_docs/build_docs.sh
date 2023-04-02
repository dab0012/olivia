#!/bin/bash

# This script builds the documentation for the olivia_finder package.

cd olivia_finder/build_docs

rm -rf docs/*

# Generate the documentation for the olivia_finder package.
make html

# Copy the documentation to the docs folder.
cp -r build/html/* ../../docs/
rm -r build