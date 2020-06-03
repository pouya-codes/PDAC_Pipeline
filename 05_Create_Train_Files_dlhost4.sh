#!/bin/bash
#SBATCH --job-name PDAC_train_files
#SBATCH --cpus-per-task 1
#SBATCH --output /home/poahmadvand/ml/slurm/create_trainfile.%j.out
#SBATCH --error /home/poahmadvand/ml/slurm/create_trainfile.%j.err
#SBATCH -w dlhost04
#SBATCH -p rtx5000
#SBATCH --gres=gpu:1
#SBATCH --time=4-90:00:00
#SBATCH --chdir /projects/ovcare/classification/pouya/components/docker_create_training_files
# 05_Create_Train_Files_dlhost4.sh

source /home/poahmadvand/py2env/bin/activate

python app.py --seed 1 --chunk_file_location "/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256_2/chunks.json" --output_location "/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/training_chunks_1.json" --training_chunks "0_1" --validation_chunks "2" --testing_chunks "2" --number_of_patches "1000000_200000_200000" --linker_location "/projects/ovcare/classification"
