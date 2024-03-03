#!/bin/python3

from pathlib import Path
import subprocess
import os
import shutil
import sys

args = sys.argv
if len(args) != 3:
    print(f"Usage: {args[0]} [list_file] [out_dir]")
    exit(-1)
file_list = Path(args[1])
out_dir = Path(args[2])

with file_list.open() as f:
    for line in f.readlines():
        line = line.rstrip()
        print(f"--> {line}")
        file = Path(line)                                                           # /media/bruno/BU2/FAE_20231026_002/NINJAV_S001_S001_T002.MOV
        out_file = Path(*file.parts[-2:])                                           # FAE_20231026_002/NINJAV_S001_S001_T002.MOV
        out_file = Path(out_dir / out_file.parent / Path(out_file.stem + '.mp4'))   # out/DD2/FAE_20231026_002/NINJAV_S001_S001_T002.mp4
        tmp_file = f"tmp/{out_file.name}"                                           # tmp/NINJAV_S001_S001_T002.mp4
        os.system(f"rm -rf tmp/*")
        print("Duration: ", end="")
        os.system(f"ffprobe -i {file} -show_entries format=duration -v quiet -of csv=\"p=0\"")
        command = f"ffpb -i {line} -c:v libx264 -pix_fmt yuv420p -crf 20 -map v:0 -map a:0 -c:a aac -map_channel 0.0.2 -b:a 128k -vf \"scale=960:540\"  {tmp_file}"
        print(command)
        errors = subprocess.call(command, shell=True)
        assert not errors
        out_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmp_file, out_file.parent)
        print("\n\n")
