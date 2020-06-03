#! /bin/bash
touch run_slerm
echo "#! /bin/bash
#SBATCH --job-name downsample_data_slurm
#SBATCH --cpus-per-task 1
#SBATCH --output /home/poahmadvand/ml/slurm/downsample_data.%j.out
#SBATCH --error /home/poahmadvand/ml/slurm/downsample_data.%j.err
#SBATCH -w dlhost02
#SBATCH -p dgxV100
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00 --wait

singularity run -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/work"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/work"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024"" -B ""/projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline/02_Preprocess.json"":""/projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline/02_Preprocess.json""  -B /projects/ovcare/classification/pouya/components/docker_downsample_data:$PWD/ /projects/ovcare/classification/pouya/components/docker_downsample_data/docker_downsample_data_latest.sif --config_file_location ""/projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline/02_Preprocess.json"" " > run_slerm
sbatch run_slerm 