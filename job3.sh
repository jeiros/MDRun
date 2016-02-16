#PBS -N job3
#PBS -l select=1
#PBS -l ncpus=1:ngpus=1
#PBS -l walltime=192:00:0
#PBS -l host=cx1-51-6-1
#PBS -q pqigould
#PBS -M je714@ic.ac.uk
#PBS -m abe

module load cuda/6.5.19

prevrst=WT-ff14SB_run8_0010-0020ns.rst
prmtop=WT-ff14SB_hmr.prmtop
prevsim=0010-0020
sim=0020-0030

cd /tmp/pbs.${PBS_JOBID}
cp /work/je714/WT/05_Prod.in .
cp /work/je714/WT/${prevrst} .
cp /work/je714/WT/${prmtop} .

pbsexec -grace 30 /home/igould/pmemd.cuda_SPFP -O -i 05_Prod.in \ 
    -o WT-ff14SB_run8_${sim}ns.out -c ${prevrst} -p ${prmtop} \ 
    -r WT-ff14SB_run8_${sim}ns.rst -x WT-ff14SB_run8_${sim}ns.nc

cp /tmp/pbs.${JOB_ID}/WT-ff14SB_run8_${sim}ns.rst /work/je714/WT/
rm /tmp/pbs.${JOB_ID}/${prevrst}
tar -zcvf /work/je714/WT/results/WT-ff14SB_run8_${sim}ns.tgz *

scp /work/je714/WT/results/WT-ff14SB_run8_${sim}ns.tgz \ 
	je714@ch-knuth.ch.ic.ac.uk:/Users/je714/Troponin/IAN_Troponin/completehowarthcut/salted/ff14SB/run8/