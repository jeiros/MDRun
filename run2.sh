#PBS -N job2
#PBS -lselect=1
#PBS -l ncpus=1:ngpus=1
#PBS -l walltime=192:00:0
#PBS -l host=cx1-51-6-1
#PBS -q pqigould
#PBS -M je714@ic.ac.uk
#PBS -m abe
module load cuda/6.5.19
prevrst=WT_cTn_0000-0050ns.rst
prmtop=WT_cTn.prmtop
cd /tmp/pbs.$PBS_JOBID
cp /work/je714/WT/*.in .
cp /work/je714/WT/${prevrst} .
cp /work/je714/WT/${prmtop} .
pbsexec -grace 15 /home/igould/pmemd.cuda_SPFP -O -i 05_Prod.in \ 
    -o WT_cTn_0050-0100ns.out -c ${prevrst} -p ${prmtop} \ 
    -r WT_cTn_0050-0100ns.rst -x WT_cTn_0050-0100ns.nc