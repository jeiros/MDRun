#PBS -N job1
#PBS -l select=1
#PBS -l ncpus=1:ngpus=1
#PBS -l walltime=192:00:0
#PBS -l host=cx1-51-6-1
#PBS -q pqigould
#PBS -M je714@ic.ac.uk
#PBS -m abe

module load cuda/6.5.19

inpcrd=WT-ff14SB.inpcrd
prmtop=WT-ff14SB_hmr.prmtop
sim=0000-0010

cd /tmp/pbs.${PBS_JOBID}
cp /work/je714/WT/*.in .
cp /work/je714/WT/${inpcrd} .
cp /work/je714/WT/${prmtop} .

/home/igould/pmemd.cuda_SPFP -O -i premin.in \ 
    -o premin.out -c ${inpcrd} -p ${prmtop} \ 
    -r premin.rst -ref ${inpcrd}

/home/igould/pmemd.cuda_SPFP -O -i sandermin1.in \ 
    -o sandermin1.out -c premin.rst -p ${prmtop} \ 
    -r sandermin1.rst

/home/igould/pmemd.cuda_SPFP -O -i 02_Heat.in \ 
    -o 02_Heat.out -c sandermin1.rst -p ${prmtop} \ 
    -r 02_Heat.rst -ref sandermin1.rst -x 02_Heat.nc

/home/igould/pmemd.cuda_SPFP -O -i 03_Heat2.in \ 
    -o 03_Heat2.out -c 02_Heat.rst -p ${prmtop} \ 
    -r 03_Heat2.rst -ref 02_Heat.rst -x 03_Heat2.nc

pbsexec -grace 30 /home/igould/pmemd.cuda_SPFP -O -i 05_Prod.in \ 
    -o WT-ff14SB_run8_${sim}ns.out -c 03_Heat2.rst -p ${prmtop} \ 
    -r WT-ff14SB_run8_${sim}ns.rst -x WT-ff14SB_run8_${sim}ns.nc

cp /tmp/pbs.${JOB_ID}/WT-ff14SB_run8_${sim}ns.rst /work/je714/WT/
rm /tmp/pbs.${JOB_ID}/${inpcrd}
tar -zcvf /work/je714/WT/results/WT-ff14SB_run8_${sim}ns.tgz *

scp /work/je714/WT/results/WT-ff14SB_run8_${sim}ns.tgz \ 
	je714@ch-knuth.ch.ic.ac.uk:/Users/je714/Troponin/IAN_Troponin/completehowarthcut/salted/ff14SB/run8/