import os
import subprocess
import signal

processes = {}

def list_scripts(directory):
    return [f for f in os.listdir(directory) if f.endswith('.sh') or f.endswith('.py')]

def get_log_path(script, log_dir):
    return os.path.join(log_dir, f"{script}.log")

def start_script(script, scripts_dir, logs_dir):
    script_path = os.path.join(scripts_dir, script)
    log_path = get_log_path(script, logs_dir)

    if not os.path.exists(script_path):
        return None

    
    log_file = open(log_path, 'a', buffering=1)

    if script.endswith('.sh'):
        
        cmd = ['stdbuf', '-oL', 'bash', script_path]
    else:
        
        cmd = ['python3', '-u', script_path]

    p = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        shell=False
    )

    
    processes[script] = (p, log_file)
    return p

def stop_script(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"Erro ao tentar parar processo {pid}: {e}")

def cleanup_script(script):
    if script in processes:
        p, log_file = processes.pop(script)
        
        log_file.close()