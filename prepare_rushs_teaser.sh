#!/bin/bash
./bash_convert.py liste-teaser.txt /media/bruno/Elements/h265/ --options='-c:v libx265 -pix_fmt yuv422p10le -crf 5 -map v:0 -map a:0 -c:a aac -map_channel 0.0.2 -b:a 40k -vf "scale=1920:1080"' --keep_path_elements=3 --ffmpeg_command=ffpb
