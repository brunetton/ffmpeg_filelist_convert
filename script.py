#!/bin/python3

"""
Usage:
    {self_filename} LIST_FILE OUT_DIR [--options=<ffmpeg_options>]
"""

from docopt import docopt
import subprocess
import os
import shutil
import sys

from pathlib import Path

args = docopt(__doc__.format(self_filename=Path(__file__).name))

out_dir = Path(args['OUT_DIR'])
list_file = Path(args['LIST_FILE'])

ffmpeg_options = '-c:v libx264 -pix_fmt yuv420p -crf 20 -map v:0 -map a:0 -c:a aac -map_channel 0.0.2 -b:a 128k -vf "scale=960:540"'
if args['--options']:
    ffmpeg_options = args['--options']
    print(f"Using ffmpeg options: {ffmpeg_options}")

with list_file.open() as f:
    for line in f.readlines():
        line = line.rstrip()
        if line == '':
            continue
        file = Path(line)                                                           # /media/bruno/BU2/FAE_20231026_002/NINJAV_S001_S001_T002.MOV
        out_file = Path(*file.parts[-2:])                                           # FAE_20231026_002/NINJAV_S001_S001_T002.MOV
        out_file = Path(out_dir / out_file.parent / Path(out_file.stem + '.mp4'))   # out/DD2/FAE_20231026_002/NINJAV_S001_S001_T002.mp4
        print(f"{line}  ->  {out_file}")
        tmp_file = f"tmp/{out_file.name}"                                           # tmp/NINJAV_S001_S001_T002.mp4
        os.system(f"rm -rf tmp/*")
        duration = subprocess.check_output(f"ffprobe -i {file} -show_entries format=duration -v quiet -of csv=\"p=0\"", shell=True)
        print("Duration: {0:.1f}m".format(float(duration.decode('utf8')) / 60))
        command = f"ffpb -i {line} {ffmpeg_options} {tmp_file}"
        print(command)
        errors = subprocess.call(command, shell=True)
        assert not errors
        out_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmp_file, out_file.parent)
        print("\n\n")
