#!/bin/bash
# Iterates over the submission files and launches them sequentially with 
# qsub.
first=true
for file in *job*.pbs; do
    if [ "$first" = true ]; then
        first=false
        ID=$(qsub $file)
    else
        ID=$(qsub -W depend=afterok:$ID $file)
    fi
done
