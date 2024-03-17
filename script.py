#!/usr/bin/env python3

"""
Usage:
    {self_filename} LIST_FILE OUT_DIR [--options=<ffmpeg_options>] [options]

Options:
    --simulate                      Do not actually convert files, only print commands that would be executed
    --keep_path_elements=<n>        [default: 2]
    --on_exists=<action>            (skip|overwrite) [default: skip]
    --ffmpeg_command=<command>      ffmpeg binary name [default: ffmpeg]
"""

from docopt import docopt
import subprocess
import os
import shutil
import sys

from pathlib import Path

args = docopt(__doc__.format(self_filename=Path(__file__).name))
# print(args)

out_dir = Path(args['OUT_DIR'])
list_file = Path(args['LIST_FILE'])

ffmpeg_options = '-c:v libx264 -pix_fmt yuv420p -crf 20 -map v:0 -map a:0 -c:a aac -map_channel 0.0.2 -b:a 128k -vf "scale=960:540"'
if args['--options']:
    ffmpeg_options = args['--options']
    print(f"Using ffmpeg options: {ffmpeg_options}")
assert args['--on_exists'] in ['skip', 'overwrite']
skip_or_overwrite = args['--on_exists']
ffmpeg_command = args['--ffmpeg_command']

with list_file.open() as f:
    for line in f.readlines():
        line = line.rstrip()
        if line == '':
            continue
        file = Path(line)                                                           # /media/bruno/BU2/FAE_20231026_002/NINJAV_S001_S001_T002.MOV
        nb_path_elements = int(args['--keep_path_elements'])
        out_file = Path(*file.parts[-nb_path_elements:])                            # DD1/FAE_20231026_002/NINJAV_S001_S001_T002.MOV (si 3 elements)
        out_file = Path(out_dir / out_file.parent / Path(out_file.stem + '.mp4'))   # /path/to/output/DD1/FAE_20231026_002/NINJAV_S001_S001_T002.mp4
        print(f"{line}  ->  {out_file}")
        # If output file already exists
        if out_file.exists():
            print(f"==> {out_file} already exists, ", end='')
            if skip_or_overwrite == 'skip':
                print('ignore this file and continue conversion')
                continue
            elif skip_or_overwrite == 'overwrite':
                out_file.unlink()
                print('replacing dersination')
        tmp_file = f"tmp/{out_file.name}"                                           # tmp/NINJAV_S001_S001_T002.mp4
        os.system(f"rm -rf tmp/*")
        duration = subprocess.check_output(f"ffprobe -i {file} -show_entries format=duration -v quiet -of csv=\"p=0\"", shell=True)
        print("Duration: {0:.1f}m".format(float(duration.decode('utf8')) / 60))
        command = f"{ffmpeg_command} -i {line} {ffmpeg_options} {tmp_file}"
        print(command)
        # Convertion
        if not args['--simulate']:
            errors = subprocess.call(command, shell=True)
            assert not errors
            out_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(tmp_file, out_file.parent)
        print("\n\n")
