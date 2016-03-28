#PBS -lselect=1:ncpus=1:ngpus=1:mem=1000mb:gpu_type=K80
#PBS -lwalltime=72:0:0
#PBS -q gpgpu
#PBS -M je714@ic.ac.uk
#PBS -m abe

prmtop=noCAL_WT-ff14SB_25-20-35Abox_hmr.prmtop
inpcrd=noCAL_WT-ff14SB_25-20-35Abox.inpcrd

cd /tmp/pbs.${PBS_JOBID}
cp /work/je714/noCAL_WT/run10/*.in .
cp /work/je714/noCAL_WT/run10/${inpcrd} .
cp /work/je714/noCAL_WT/run10/${prmtop} .

/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i premin.in -o premin.out -c ${inpcrd} -p ${prmtop} -r premin.rst -ref ${inpcrd}
/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i sandermin1.in -o sandermin1.out -c premin.rst -p ${prmtop} -r sandermin1.rst
/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i 02_Heat.in -o 02_Heat.out -c sandermin1.rst -p ${prmtop} -r 02_Heat.rst -ref sandermin1.rst -x 02_Heat.nc
/home/igould/newamber/amber/bin/pmemd.cuda_SPFP -O -i 03_Heat2.in -o 03_Heat2.out -c 02_Heat.rst -p ${prmtop} -r 03_Heat2.rst -ref 02_Heat.rst -x 03_Heat2.nc
