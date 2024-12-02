#!/bin/bash
clear
echo
echo
# echo "Enter number of test runs"
# read runs 
runs=3
echo 
echo
echo "we are going to run $runs tests"
for i in $(seq 1 $runs); 
do   
    python3 app.py ./tests/prompt${i}.json
    mv output.txt ./tests/output/output${i}.txt
done
