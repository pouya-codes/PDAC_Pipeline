#!/bin/bash
#SBATCH --job-name lgg_train_files
#SBATCH --cpus-per-task 1
#SBATCH --output /home/poahmadvand/ml/slurm/%j.out
#SBATCH --error /home/poahmadvand/ml/slurm/%j.out
#SBATCH -w dlhost02
#SBATCH -p dgxV100
#SBATCH --gres=gpu:1
#SBATCH --time=4-90:00:00
#SBATCH --chdir /projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline

source /home/poahmadvand/py2env/bin/activate

kronos run \
	-c $PWD/../ \
	-y 06_train.yaml \
	--no_prefix 
