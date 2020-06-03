#! /bin/bash
touch run_slerm
echo "#! /bin/bash
#SBATCH --job-name sort_patches_by_label_slurm
#SBATCH --cpus-per-task 1
#SBATCH --output /home/poahmadvand/ml/slurm/sort_patches_by_label.%j.out
#SBATCH --error /home/poahmadvand/ml/slurm/sort_patches_by_label.%j.err
#SBATCH -w dlhost02
#SBATCH -p dgxV100
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00 --wait

singularity run -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256_sorted"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256_sorted"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/labels_file.txt"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/labels_file.txt""  -B /projects/ovcare/classification/pouya/components/docker_sort_patches_by_label:$PWD/ /projects/ovcare/classification/pouya/components/docker_sort_patches_by_label/docker_sort_patches_by_label_latest.sif --patch_location ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256"" --sorted_location ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256_sorted"" --labels_file_location ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/labels_file.txt"" " > run_slerm
sbatch run_slerm 