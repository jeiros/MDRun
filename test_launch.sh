#!/bin/bash

FIRST=$(qsub job1.pbs)
echo $FIRST
SECOND=$(qsub -W depend=afterok:$FIRST job2.pbs)
echo $SECOND
THIRD=$(qsub -W depend=afterok:$SECOND job3.pbs)
echo $THIRD