#!/bin/bash
#SBATCH --job-name PDAC_train_files
#SBATCH --cpus-per-task 1
#SBATCH --output /home/poahmadvand/ml/slurm/create_trainfile.%j.out
#SBATCH --error /home/poahmadvand/ml/slurm/create_trainfile.%j.err
#SBATCH -w dlhost04
#SBATCH -p rtx5000
#SBATCH --gres=gpu:1
#SBATCH --time=4-90:00:00
#SBATCH --chdir /projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline
# 05_Create_Train_Files.sh

source /home/poahmadvand/py2env/bin/activate

kronos run \
	-c $PWD/../ \
	-y 05_Create_Train_Files.yaml \
	--no_prefix 
