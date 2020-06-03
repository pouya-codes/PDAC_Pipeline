#! /bin/bash
touch run_slerm
echo "#! /bin/bash
#SBATCH --job-name patch_annotation_extraction_slurm
#SBATCH --cpus-per-task 1
#SBATCH --output /projects/ovcare/classification/pouya/logs/local_ec_100_extract.%j.out
#SBATCH --error /projects/ovcare/classification/pouya/local_ec_100_extract.%j.err
#SBATCH -w dlhost02
#SBATCH -p dgxV100
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00 --wait
#SBATCH --mem=100G
singularity run -B ""/projects/ovcare/WSI"":""/projects/ovcare/WSI"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/slides"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/slides"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024"" -B ""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/Annotated"":""/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/Annotated"" -B ""/projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline/01_Extract_Pathes.json"":""/projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline/01_Extract_Pathes.json""  -B /projects/ovcare/classification/pouya/components/docker_patch_annotation_extraction:$PWD/ /projects/ovcare/classification/pouya/components/docker_patch_annotation_extraction/docker_patch_annotation_extraction_latest.sif --linker_location ""/projects/ovcare/WSI"" --config_file_location ""/projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline/01_Extract_Pathes.json"" " > run_slerm
sbatch run_slerm 