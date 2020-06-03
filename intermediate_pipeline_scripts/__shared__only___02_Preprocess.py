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
TASK_DIVIDE_WORK_component = kronos_component_singularity_main.Component('kronos_component_singularity', component_parent_dir=args.components_dir)
TASK_DIVIDE_WORK_task = Task('TASK_DIVIDE_WORK', TASK_DIVIDE_WORK_component)
TASK_DIVIDE_WORK_task.update_comp_args(__pipeline__work_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/work', __pipeline__slurm_max_time='10:00:00', __pipeline__slurm_error='/home/poahmadvand/ml/slurm/divide_work.%j.err', __pipeline__slurm_machine='dlhost02', __pipeline__N=3, __pipeline__data_location='/projects/ovcare/classification/Diagnostic_TCGA_PDAC_cases/patches_1024', __pipeline__slurm_job_name='divide_work_slurm', __pipeline__slurm_num_cpu=30, __pipeline__slurm_num_gpu=1, __pipeline__slurm_output='/home/poahmadvand/ml/slurm/divide_work.%j.out', __pipeline__singularity_image='/projects/ovcare/classification/pouya/components/docker_divide_work/docker_divide_work_latest.sif', __pipeline__parameters=None, __pipeline__slurm_queue='dgxV100', __pipeline__output_files=None, )
TASK_DIVIDE_WORK_prefix = rm.get_filename_prefix('TASK_DIVIDE_WORK')
TASK_DIVIDE_WORK_task.update_comp_output_filenames(TASK_DIVIDE_WORK_prefix, rm.outputs_dir, args.no_prefix)
TASK_DIVIDE_WORK_task.update_comp_env_vars({})
TASK_DIVIDE_WORK_task.update_comp_reqs({'docker': '__REQUIRED__'})

TASK_DOWNSAMPLE_DATA_component = kronos_component_singularity_main.Component('kronos_component_singularity', component_parent_dir=args.components_dir)
TASK_DOWNSAMPLE_DATA_task = Task('TASK_DOWNSAMPLE_DATA', TASK_DOWNSAMPLE_DATA_component)
TASK_DOWNSAMPLE_DATA_task.update_comp_args(__pipeline__config_file_location='/projects/ovcare/classification/pouya/components/PDAC_Binary_Pipeline/02_Preprocess.json', __pipeline__slurm_max_time='10:00:00', __pipeline__slurm_error='/home/poahmadvand/ml/slurm/downsample_data.%j.err', __pipeline__slurm_machine='dlhost02', __pipeline__slurm_job_name='downsample_data_slurm', __pipeline__slurm_num_cpu=30, __pipeline__slurm_num_gpu=1, __pipeline__slurm_output='/home/poahmadvand/ml/slurm/downsample_data.%j.out', __pipeline__singularity_image='/projects/ovcare/classification/pouya/components/docker_downsample_data/docker_downsample_data_latest.sif', __pipeline__parameters=None, __pipeline__slurm_queue='dgxV100', __pipeline__output_files=None, )
TASK_DOWNSAMPLE_DATA_prefix = rm.get_filename_prefix('TASK_DOWNSAMPLE_DATA')
TASK_DOWNSAMPLE_DATA_task.update_comp_output_filenames(TASK_DOWNSAMPLE_DATA_prefix, rm.outputs_dir, args.no_prefix)
TASK_DOWNSAMPLE_DATA_task.update_comp_env_vars({})
TASK_DOWNSAMPLE_DATA_task.update_comp_reqs({'docker': '__REQUIRED__'})

#================================================================================
#ruffus pipeline
#--------------------------------------------------------------------------------
@ruffus.follows(*[])
@ruffus.parallel(TASK_DIVIDE_WORK_component.component_name, 'TASK_DIVIDE_WORK', [])
@ruffus.check_if_uptodate(rm.sentinel_file_exists)
@LogWarnErr(l)
@LogInfo(l)
def kronos_component_singularity_TASK_DIVIDE_WORK_function(*inargs):
    component_name, task_name, _ = inargs
    print '%s for %s started in %s pipeline' % (task_name, component_name, args.pipeline_name)
    run_script = rm.generate_script(TASK_DIVIDE_WORK_task, None, None)
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

@ruffus.follows(*[kronos_component_singularity_TASK_DIVIDE_WORK_function])
@ruffus.parallel(TASK_DOWNSAMPLE_DATA_component.component_name, 'TASK_DOWNSAMPLE_DATA', ['TASK_DIVIDE_WORK'])
@ruffus.check_if_uptodate(rm.sentinel_file_exists)
@LogWarnErr(l)
@LogInfo(l)
def kronos_component_singularity_TASK_DOWNSAMPLE_DATA_function(*inargs):
    component_name, task_name, _ = inargs
    print '%s for %s started in %s pipeline' % (task_name, component_name, args.pipeline_name)
    run_script = rm.generate_script(TASK_DOWNSAMPLE_DATA_task, None, None)
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

@ruffus.follows(*[kronos_component_singularity_TASK_DOWNSAMPLE_DATA_function, ])
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
