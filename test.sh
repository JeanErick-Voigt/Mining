#!/bin/bash

for i in ../test_maps/test_map-*; do 
    echo $i: $(../world.py $i $i $1 | grep "Total")
done
