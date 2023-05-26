#!/bin/bash

mkdir tmp
cat results/results.tar.bz2_part_* > tmp/results.tar.bz2
tar -xvjf tmp/results.tar.bz2 -C tmp
rm -rf results
rm tmp/results.tar.bz2
mv tmp/* ./
rm -rf tmp