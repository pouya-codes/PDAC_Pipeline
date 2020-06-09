#================================================================================
#import python modules as well as pipelinui
#--------------------------------------------------------------------------------
import ruffus
import traceback
import sys
import time
import os
from multiprocessing import Queue

#================================================================================
#import factory modules
#--------------------------------------------------------------------------------
import kronos.pipelineui
from kronos.run_manager import RunManager
from kronos.job_manager import DrmaaJobManager, SgeJobManager, LocalJobManager
from kronos.helpers import JobFailureError, flushqueue
from kronos.logger import PipelineLogger, LogWarnErr, LogInfo
from kronos.utils import Task

#================================================================================
#initialization
#--------------------------------------------------------------------------------
args = kronos.pipelineui.args
rm = RunManager(args.run_id, args.pipeline_name, args.working_dir)
ljm = LocalJobManager(rm.logs_dir, rm.outputs_dir)
pl = PipelineLogger()
l = pl.get_logger(args.pipeline_name, args.log_file)

#================================================================================
#environment preparations
#--------------------------------------------------------------------------------
sys.path.insert(0, args.components_dir)
job_rcs = Queue()

#================================================================================
#import components
#--------------------------------------------------------------------------------
from kronos_component_singularity import component_main as kronos_component_singularity_main

#================================================================================
#generating tasks
#--------------------------------------------------------------------------------
TASK_CREATE_TRAINING_FILES_2_component = kronos_component_singularity_main.Component('kronos_component_singularity', component_parent_dir=args.components_dir)
TASK_CREATE_TRAINING_FILES_2_task = Task('TASK_CREATE_TRAINING_FILES_2', TASK_CREATE_TRAINING_FILES_2_component)
TASK_CREATE_TRAINING_FILES_2_task.update_comp_args(__pipeline__number_of_patches='1000000_200000_200000', __pipeline__validation_chunks='0', __pipeline__slurm_max_time='10:00:00', __pipeline__slurm_error='/home/poahmadvand/ml/slurm/create_training_files_2.%j.err', __pipeline__slurm_machine='dlhost04', __pipeline__chunk_file_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256_sorted/chunks.json', __pipeline__linker_location='/projects/ovcare/classification', __pipeline__training_chunks='1_2', __pipeline__slurm_job_name='create_training_files_slurm', __pipeline__output_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/training_chunks_2.json', __pipeline__slurm_num_cpu=2, __pipeline__seed=1, __pipeline__parameters=None, __pipeline__slurm_num_gpu=2, __pipeline__slurm_output='/home/poahmadvand/ml/slurm/create_training_files_2.%j.out', __pipeline__singularity_image='/projects/ovcare/classification/pouya/components/docker_create_training_files/docker_create_training_files.sif', __pipeline__testing_chunks='0', __pipeline__slurm_queue='rtx5000', __pipeline__output_files=None, )
TASK_CREATE_TRAINING_FILES_2_prefix = rm.get_filename_prefix('TASK_CREATE_TRAINING_FILES_2')
TASK_CREATE_TRAINING_FILES_2_task.update_comp_output_filenames(TASK_CREATE_TRAINING_FILES_2_prefix, rm.outputs_dir, args.no_prefix)
TASK_CREATE_TRAINING_FILES_2_task.update_comp_env_vars({})
TASK_CREATE_TRAINING_FILES_2_task.update_comp_reqs({'docker': '__REQUIRED__'})

TASK_CREATE_TRAINING_FILES_3_component = kronos_component_singularity_main.Component('kronos_component_singularity', component_parent_dir=args.components_dir)
TASK_CREATE_TRAINING_FILES_3_task = Task('TASK_CREATE_TRAINING_FILES_3', TASK_CREATE_TRAINING_FILES_3_component)
TASK_CREATE_TRAINING_FILES_3_task.update_comp_args(__pipeline__number_of_patches='10000000_200000_200000', __pipeline__validation_chunks='1', __pipeline__slurm_max_time='10:00:00', __pipeline__slurm_error='/home/poahmadvand/ml/slurm/create_training_files_3.%j.err', __pipeline__slurm_machine='dlhost04', __pipeline__chunk_file_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256_sorted/chunks.json', __pipeline__linker_location='/projects/ovcare/classification/', __pipeline__training_chunks='0_2', __pipeline__slurm_job_name='create_training_files_slurm', __pipeline__output_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/training_chunks_3.json', __pipeline__slurm_num_cpu=2, __pipeline__seed=1, __pipeline__parameters=None, __pipeline__slurm_num_gpu=2, __pipeline__slurm_output='/home/poahmadvand/ml/slurm/create_training_files_3.%j.out', __pipeline__singularity_image='/projects/ovcare/classification/pouya/components/docker_create_training_files/docker_create_training_files.sif', __pipeline__testing_chunks='1', __pipeline__slurm_queue='rtx5000', __pipeline__output_files=None, )
TASK_CREATE_TRAINING_FILES_3_prefix = rm.get_filename_prefix('TASK_CREATE_TRAINING_FILES_3')
TASK_CREATE_TRAINING_FILES_3_task.update_comp_output_filenames(TASK_CREATE_TRAINING_FILES_3_prefix, rm.outputs_dir, args.no_prefix)
TASK_CREATE_TRAINING_FILES_3_task.update_comp_env_vars({})
TASK_CREATE_TRAINING_FILES_3_task.update_comp_reqs({'docker': '__REQUIRED__'})

TASK_CREATE_TRAINING_FILES_1_component = kronos_component_singularity_main.Component('kronos_component_singularity', component_parent_dir=args.components_dir)
TASK_CREATE_TRAINING_FILES_1_task = Task('TASK_CREATE_TRAINING_FILES_1', TASK_CREATE_TRAINING_FILES_1_component)
TASK_CREATE_TRAINING_FILES_1_task.update_comp_args(__pipeline__number_of_patches='1000000_200000_200000', __pipeline__validation_chunks='2', __pipeline__slurm_max_time='10:00:00', __pipeline__slurm_error='/home/poahmadvand/ml/slurm/create_training_files_1.%j.err', __pipeline__slurm_machine='dlhost04', __pipeline__chunk_file_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_256_sorted/chunks.json', __pipeline__linker_location='/projects/ovcare/classification', __pipeline__training_chunks='0_1', __pipeline__slurm_job_name='create_training_files_slurm', __pipeline__output_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/training_chunks_1.json', __pipeline__slurm_num_cpu=2, __pipeline__seed=1, __pipeline__parameters=None, __pipeline__slurm_num_gpu=2, __pipeline__slurm_output='/home/poahmadvand/ml/slurm/create_training_files_1.%j.out', __pipeline__singularity_image='/projects/ovcare/classification/pouya/components/docker_create_training_files/docker_create_training_files.sif', __pipeline__testing_chunks='2', __pipeline__slurm_queue='rtx5000', __pipeline__output_files=None, )
TASK_CREATE_TRAINING_FILES_1_prefix = rm.get_filename_prefix('TASK_CREATE_TRAINING_FILES_1')
TASK_CREATE_TRAINING_FILES_1_task.update_comp_output_filenames(TASK_CREATE_TRAINING_FILES_1_prefix, rm.outputs_dir, args.no_prefix)
TASK_CREATE_TRAINING_FILES_1_task.update_comp_env_vars({})
TASK_CREATE_TRAINING_FILES_1_task.update_comp_reqs({'docker': '__REQUIRED__'})

#================================================================================
#ruffus pipeline
#--------------------------------------------------------------------------------
@ruffus.follows(*[])
@ruffus.parallel(TASK_CREATE_TRAINING_FILES_2_component.component_name, 'TASK_CREATE_TRAINING_FILES_2', [])
@ruffus.check_if_uptodate(rm.sentinel_file_exists)
@LogWarnErr(l)
@LogInfo(l)
def kronos_component_singularity_TASK_CREATE_TRAINING_FILES_2_function(*inargs):
    component_name, task_name, _ = inargs
    print '%s for %s started in %s pipeline' % (task_name, component_name, args.pipeline_name)
    run_script = rm.generate_script(TASK_CREATE_TRAINING_FILES_2_task, None, None)
    job_name = rm.get_filename_prefix(task_name)
    time.sleep(1)
    try:
        rc = ljm.run_job(cmd=run_script, job_name=job_name)
        job_rcs.put(rc)
        if rc == 0:
            rm.generate_sentinel_file(task_name)
    except KeyboardInterrupt:
        raise
    except:
        job_rcs.put(98)
        traceback.print_exc()

@ruffus.follows(*[])
@ruffus.parallel(TASK_CREATE_TRAINING_FILES_3_component.component_name, 'TASK_CREATE_TRAINING_FILES_3', [])
@ruffus.check_if_uptodate(rm.sentinel_file_exists)
@LogWarnErr(l)
@LogInfo(l)
def kronos_component_singularity_TASK_CREATE_TRAINING_FILES_3_function(*inargs):
    component_name, task_name, _ = inargs
    print '%s for %s started in %s pipeline' % (task_name, component_name, args.pipeline_name)
    run_script = rm.generate_script(TASK_CREATE_TRAINING_FILES_3_task, None, None)
    job_name = rm.get_filename_prefix(task_name)
    time.sleep(1)
    try:
        rc = ljm.run_job(cmd=run_script, job_name=job_name)
        job_rcs.put(rc)
        if rc == 0:
            rm.generate_sentinel_file(task_name)
    except KeyboardInterrupt:
        raise
    except:
        job_rcs.put(98)
        traceback.print_exc()

@ruffus.follows(*[])
@ruffus.parallel(TASK_CREATE_TRAINING_FILES_1_component.component_name, 'TASK_CREATE_TRAINING_FILES_1', [])
@ruffus.check_if_uptodate(rm.sentinel_file_exists)
@LogWarnErr(l)
@LogInfo(l)
def kronos_component_singularity_TASK_CREATE_TRAINING_FILES_1_function(*inargs):
    component_name, task_name, _ = inargs
    print '%s for %s started in %s pipeline' % (task_name, component_name, args.pipeline_name)
    run_script = rm.generate_script(TASK_CREATE_TRAINING_FILES_1_task, None, None)
    job_name = rm.get_filename_prefix(task_name)
    time.sleep(1)
    try:
        rc = ljm.run_job(cmd=run_script, job_name=job_name)
        job_rcs.put(rc)
        if rc == 0:
            rm.generate_sentinel_file(task_name)
    except KeyboardInterrupt:
        raise
    except:
        job_rcs.put(98)
        traceback.print_exc()

@ruffus.follows(*[kronos_component_singularity_TASK_CREATE_TRAINING_FILES_2_function, kronos_component_singularity_TASK_CREATE_TRAINING_FILES_3_function, kronos_component_singularity_TASK_CREATE_TRAINING_FILES_1_function, ])
def __last_task___function():
    pass

#================================================================================
#main body
#--------------------------------------------------------------------------------
try:
    if not args.print_only:
        ruffus.pipeline_run(__last_task___function, multithread=args.num_jobs, verbose=0)
    else:
        cwd = os.getcwd()
        os.chdir(rm.pipeline_dir)
        ruffus.pipeline_printout_graph(args.pipeline_name + '.' + args.extension, args.extension, [__last_task___function], draw_vertically = args.draw_vertically, no_key_legend = args.no_key_legend, user_colour_scheme = {'colour_scheme_index': 1, 'Pipeline': {'fontcolor': '"#FF3232"'}, 'Task to run': {'linecolor': '"#0044A0"'}, 'Key': {'fontcolor': 'Red', 'fillcolor': '"#F6F4F4"'}, 'Final target': {'fontcolor': 'black', 'fillcolor': '"#EFA03B"', 'dashed': 0}})
        os.chdir(cwd)

    lrc = flushqueue(job_rcs)
    if all(rc == 0 for rc in lrc):
        EXIT_CODE = 0
    else:
        EXIT_CODE = 98

except:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    ##exception object is of type <class 'ruffus.ruffus_exceptions.RethrownJobError'>.
    ##exc_obj.args[0][3] gives the message in the original exception.
    if exc_obj.args[0][3] == '(breakpoint)':
        print 'breakpoint happened in %s pipeline' % (args.pipeline_name)
        ljm.kill_all()
        EXIT_CODE = 99

    else:
        print >> sys.stderr, '{0} pipeline failed due to error: {1}, {2}'.format(args.pipeline_name, exc_type, exc_obj)
        ljm.kill_all()
        EXIT_CODE = -1

finally:
    print '{0} pipeline finished with exit code {1}'.format(args.pipeline_name, EXIT_CODE)
    sys.exit(EXIT_CODE)
