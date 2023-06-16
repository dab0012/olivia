#!/bin/bash

# --------------------------------------------------
# Pack results and split into 50MB chunks for upload
# safely to GitHub
# --------------------------------------------------

mkdir tmp
tar -cvjf tmp/results.tar.bz2 results
split -b 50M -d --suffix-length=2 tmp/results.tar.bz2 tmp/results.tar.bz2_part_
rm tmp/results.tar.bz2
rm -rf results
mv tmp results

