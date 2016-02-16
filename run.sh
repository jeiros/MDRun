#!/bin/bash

#change this to =0 to run on other GPU
export CUDA_VISIBLE_DEVICES="2"


phosptype=S1P
# prevsim=1050-1200
sim=000-135
run=run9
cluster=init
SCRIPTS=/home/je714/scripts
mkdir job

scp ./* ./job

cd job
count=${phosptype}-ff14SB_25-20-35Abox
prmtop=${count}_hmr.prmtop
inpcrd=${count}.inpcrd



/usr/local/amber/bin/pmemd.cuda_SPFP -O -i ${SCRIPTS}/premin.in -o premin_${count}_${cluster}.out -c ${inpcrd} -p ${prmtop} -r premin_${count}_${cluster}.rst  -ref ${inpcrd}

/usr/local/amber/bin/pmemd.cuda_SPFP -O -i ${SCRIPTS}/sandermin1.in -o sandermin_${count}_${cluster}.out -c premin_${count}_${cluster}.rst -p ${prmtop} -r sandermin1_${count}_${cluster}.rst

/usr/local/amber/bin/pmemd.cuda_SPFP -O -i ${SCRIPTS}/02_Heat.in -o 02_Heat_${count}_${cluster}.out -c sandermin1_${count}_${cluster}.rst -p ${prmtop} -r 02_Heat_${count}_${cluster}.rst -x 02_Heat_${count}_${cluster}.nc -ref sandermin1_${count}_${cluster}.rst

/usr/local/amber/bin/pmemd.cuda_SPFP -O -i ${SCRIPTS}/03_Heat2.in -o 03_Heat2_${count}_${cluster}.out -c 02_Heat_${count}_${cluster}.rst -p ${prmtop} -r 03_Heat2_${count}_${cluster}.rst -x 03_Heat2_${count}_${cluster}.nc -ref 02_Heat_${count}_${cluster}.rst

/usr/local/amber/bin/pmemd.cuda_SPFP -O -i 05_Prod.in -o 05_Prod_${cluster}.phos${phosptype}.${sim}_${run}.out -c 03_Heat2_${count}_${cluster}.rst -p ${prmtop} -r 05_Prod_${cluster}.phos${phosptype}.${sim}_${run}.rst -x 05_Prod_${cluster}.phos${phosptype}.${sim}_${run}.nc


scp ./05_Prod_${cluster}.phos${phosptype}.${sim}_${run}.rst ../

tar -zcvf ./${run}_${cluster}_${phosptype}_${sim}.tgz *

mv  ./${run}_${cluster}_${phosptype}_${sim}.tgz ../results
cd ../
rm -rf ./job/



