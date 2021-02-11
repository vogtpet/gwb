import shutil
import subprocess
from pathlib import Path

import ipyvuetify as v

from component.message import cm
from component import parameter as cp

def run_gwb_process(process, raster, params_list, title, output, offset):
    """
    run all the processes of the GWB suit according to the io
    The input and output folder will be created on the fly and deleted right afterward
    The result will be saved in the result_dir of the parameter component
    The log will be displayed to the end user and then removed
    
    Args: 
        io (GWBIo): any io inheriting from the GWBIo object
        
    Return:
        (pathlib.Path) : the path to the final .image
        (pathlib.Path) : the path to the final .csv
    """
    # create the output names 
    txt_final = cp.get_result_dir(process).joinpath(f'{process}_{raster.stem}_{title}.txt')
    tif_final = cp.get_result_dir(process).joinpath(f'{process}_{raster.stem}_{title}.tif')
    csv_final = cp.get_result_dir(process).joinpath(f'{process}_{raster.stem}_{title}.csv')
    
    # stop if already exist 
    if txt_final.is_file() and tif_final.is_file() and csv.is_file():
        output.add_live_msg(cm.gwb.file_exist.format(process.upper(), raster.stem, title), 'warning')
        return (txt_final, tif_final, csv_final)
    
    # create the tmp directories 
    tmp_dir = cp.get_tmp_dir()
    in_dir = tmp_dir.joinpath('input')
    in_dir.mkdir()
    out_dir = tmp_dir.joinpath('output')
    out_dir.mkdir()
    
    # fill the tmp dir with the raster 
    shutil.copy(raster, in_dir)
    
    # create the input file
    parameter_file = in_dir.joinpath(f'{process}-parameters.txt')
    with parameter_file.open('w') as f:
        offset_lines = ['\n' for i in range(offset-1)]
        params_lines = [str(p) + '\n' for p in params_list]
        finish_lines = ['\n']
        f.writelines(offset_lines + params_lines +finish_lines)
            
    # create the command 
    command = [
        f'GWB_{process.upper()}',
        f'-i={in_dir}',
        f'-o={out_dir}'
    ]
    
    print(' '.join(command))
    
    # set the argument of the process
    kwargs = {
        'args' : command,
        'cwd' : Path('~').expanduser(), # launch from home to avoid permissions bugs
        'stdout' : subprocess.PIPE,
        'stderr' : subprocess.PIPE,
        'universal_newlines' : True
    }
    
    # start the process 
    output.add_live_msg(cm.gwb.start.format(process.upper()))
    
    with subprocess.Popen(**kwargs) as p:
        for line in p.stdout:
            output.append_msg(line)
            
    # file in the output directory 
    out_txt = out_dir.joinpath(f'{raster.stem}_{process}', f'{raster.stem}_{process}.txt')
    out_tif = out_dir.joinpath(f'{raster.stem}_{process}', f'{raster.stem}_{process}.tif')
    out_csv = out_dir.joinpath(f'{raster.stem}_{process}', f'{raster.stem}_{process}.csv')
    out_log = out_dir.joinpath(f'{process}.log')
    
    # if log is not there, the comutation didn't even started 
    # I let the display in its current state and change the color of the output to red
    if not out_log.is_file():
        output.type = 'error'
        return ("#", "#", "#")
    
    # if the log file is the only file then it has crashed
    
    # read the log 
    with open(out_log) as f:
        log = f.read()
        
    # copy the files in the result directory 
    shutil.copy(out_txt, txt_final)
    shutil.copy(out_tif, tif_final)
    shutil.copy(out_csv, csv_final)
    
    # display the final log 
    output.add_live_msg(v.Html(tag='pre', class_='success--text d-inline', children=[log]), 'success')
    
    return (txt_final, tif_final, csv_final)
        
    
    