#!/bin/bash
#SBATCH --job-name PDAC_preprocess
#SBATCH --cpus-per-task 1
#SBATCH --output /home/poahmadvand/ml/slurm/%j.out
#SBATCH --error /home/poahmadvand/ml/slurm/%j.err
#SBATCH -w dlhost02
#SBATCH -p dgxV100
#SBATCH --gres=gpu:1
#SBATCH --time=4-90:00:00
#SBATCH --chdir /projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline

source /home/poahmadvand/py2env/bin/activate

kronos run \
	-c $PWD/../ \
	-y 02_Preprocess.yaml \
	--no_prefix 
