import subprocess


def run_apps():
    subprocess.Popen(
        ['./projecteuler/app.py',], env={'PYTHONPATH': '.'}
    )
    subprocess.Popen(
        ['./tasks/app.py',], env={'PYTHONPATH': '.'}
    )
    subprocess.Popen(
        ['./users/app.py',], env={'PYTHONPATH': '.'}
    )
