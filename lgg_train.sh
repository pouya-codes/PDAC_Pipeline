#!/bin/bash
#SBATCH --job-name lgg_train_files
#SBATCH --cpus-per-task 1
#SBATCH --output /projects/ovcare/classification/zli/ml/pipeline/slurm/%j.out
#SBATCH --error /projects/ovcare/classification/zli/ml/pipeline/slurm/%j.out
#SBATCH -w dlhost02
#SBATCH -p dgxV100
#SBATCH --gres=gpu:1
#SBATCH --time=4-90:00:00
#SBATCH --chdir /projects/ovcare/classification/zli/ml/pipeline

source /projects/ovcare/classification/zli/ml/py2env/bin/activate

kronos run \
	-c $PWD/../ \
	-y lgg_train.yaml \
	--no_prefix 
