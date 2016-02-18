#!/bin/bash

first=true
for file in *job*.sh; do
    if [ "$first" = true ]; then
        first=false
        ID=$(qsub $file)
    else
        ID=$(qsub -W depend=afterok:$ID $file)
    fi
done
