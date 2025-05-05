#!/bin/bash

#SBATCH -t 100:00:00
#SBATCH --job-name=datapro
#SBATCH -p normal
#SBATCH --export=ALL
#SBATCH --output=datapro.txt
#SBATCH --ntasks-per-node=1
#SBATCH --array=1

module load netcdf
module load python/3.11.5
source ~/py311-env/bin/activate 


python3 ./src/data_process.py $SLURM_ARRAY_TASK_ID