from pathlib import Path
import subprocess as sp
import shlex
import os
import sys
import shutil


instance_path = input('Path to MC instance: ')

mcdir = Path(instance_path)

os.chdir(Path(__file__).parent.resolve())

def run_cmd(cmd):
    sp.call(shlex.split(cmd))

# run_cmd('py -m ensurepip')

dir_to_zip = Path.cwd() / 'tmp'

if (dir_to_zip.exists()):
    shutil.rmtree(dir_to_zip)
dir_to_zip.mkdir()

num_worlds = 5
num_logs = 5

all_world_times = []

for world in (mcdir / "saves").iterdir():
    world_time = world.stat().st_mtime
    all_world_times.append(world_time)

all_world_times.sort()

for world in (mcdir / "saves").iterdir():
    if world.stat().st_mtime > all_world_times[-num_worlds]:
        shutil.copytree(world, dir_to_zip / world.name)

all_log_times = []

for log in (mcdir / "logs").iterdir():
    log_time = log.stat().st_mtime
    all_log_times.append(log_time)

all_log_times.sort()

for log in (mcdir / "logs").iterdir():
    if log.stat().st_mtime > all_log_times[-num_logs]:
        shutil.copyfile(log, dir_to_zip / world.name)


shutil.make_archive('mc_verification', 'zip',dir_to_zip)
