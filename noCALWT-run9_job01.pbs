#PBS -lselect=1:ncpus=1:ngpus=1:mem=1000mb:gpu_type=K80
#PBS -q gpgpu
#PBS -M je714@ic.ac.uk
#PBS -m abe

module load cuda/6.5.19

prmtop=noCAL_WT-ff14SB_25-20-35Abox_hmr.prmtop
sim=0000-0009

inpcrd=noCAL_WT-ff14SB_25-20-35Abox.inpcrd
cd /tmp/pbs.${PBS_JOBID}
cp /work/je714/noCAL_WT/run9/*.in .
cp /work/je714/noCAL_WT/run9/${inpcrd} .
cp /work/je714/noCAL_WT/run9/${prmtop} .

/home/igould/pmemd.cuda_SPFP -O -i premin.in -o premin.out -c ${inpcrd} -p ${prmtop} -r premin.rst -ref ${inpcrd}

/home/igould/pmemd.cuda_SPFP -O -i sandermin1.in -o sandermin1.out -c premin.rst -p ${prmtop} -r sandermin1.rst

/home/igould/pmemd.cuda_SPFP -O -i 02_Heat.in -o 02_Heat.out -c sandermin1.rst -p ${prmtop} -r 02_Heat.rst -ref sandermin1.rst -x 02_Heat.nc

/home/igould/pmemd.cuda_SPFP -O -i 03_Heat2.in -o 03_Heat2.out -c 02_Heat.rst -p ${prmtop} -r 03_Heat2.rst -ref 02_Heat.rst -x 03_Heat2.nc

pbsexec -grace 15 /home/igould/pmemd.cuda_SPFP -O -i 05_Prod.in -o noCALWT-run9_${sim}ns.out -c 03_Heat2.rst -p ${prmtop} -r noCALWT-run9_${sim}ns.rst -x noCALWT-run9_${sim}ns.nc

cp /tmp/pbs.${PBS_JOBID}/noCALWT-run9_${sim}ns.rst /work/je714/noCAL_WT/run9/
rm /tmp/pbs.${PBS_JOBID}/${inpcrd}
tar -zcvf /work/je714/noCAL_WT/run9/results/noCALWT-run9_${sim}ns.tgz *

scp /work/je714/noCAL_WT/run9/results/noCALWT-run9_${sim}ns.tgz je714@ch-knuth.ch.ic.ac.uk:/Users/je714/Troponin/IAN_Troponin/completehowarthcut/noCAL_WT/run9/
