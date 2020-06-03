#! /bin/bash
touch run_slerm
echo "#! /bin/bash
#SBATCH --job-name divide_work_slurm
#SBATCH --cpus-per-task 1
#SBATCH --output /home/poahmadvand/ml/slurm/divide_work.%j.out
#SBATCH --error /home/poahmadvand/ml/slurm/divide_work.%j.err
#SBATCH -w dlhost02
#SBATCH -p dgxV100
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00 --wait

singularity run -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/work"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/work"" -B ""/projects/ovcare/classification/cchen"":""/projects/ovcare/classification/cchen"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024""  -B /projects/ovcare/classification/pouya/components/docker_divide_work:$PWD/ /projects/ovcare/classification/pouya/components/docker_divide_work/divide_work_latest.sif --work_location ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/work"" --linker_location ""/projects/ovcare/classification/cchen"" --N 3 --data_location ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024"" " > run_slerm
sbatch run_slerm 