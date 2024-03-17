Simple & (not so) dirty ffmpeg conversion script
## Input
- a list of files to convert, this list is a text file

## Output
- converted files with ffmpeg (or another wrapper, like [ffpb](https://github.com/althonos/ffpb))
- the original directories tree can be kept (you can specify the amount of directories to keep)
- note: during conversion, a `tmp/` dir is created and used to place currently converted file

## Example

### List file
```
./source_files/DD1/FAE_20231025_001/NINJAV_S001_S001_T017.MOV
./source_files/DD1/FAE_20231025_001/NINJAV_S001_S001_T033.MOV
./source_files/DD1/FAE_20231026_002/NINJAV_S001_S001_T003.MOV
./source_files/DD1/FAE_20231026_002/NINJAV_S001_S001_T021.MOV
```

### Command
```bash
./bash_convert.py list_file.txt outdir/  --keep_path_elements=2
```

### Output
```
outdir
├── FAE_20231025_001
│   ├── NINJAV_S001_S001_T017.mp4
│   └── NINJAV_S001_S001_T033.mp4
└── FAE_20231026_002
    ├── NINJAV_S001_S001_T003.mp4
    └── NINJAV_S001_S001_T021.mp4
```

### Same example but using --keep_path_elements=3

```bash
./bash_convert.py list_file.txt outdir/  --keep_path_elements=2
```

```
outdir
└── DD1
    ├── FAE_20231025_001
    │   ├── NINJAV_S001_S001_T017.mp4
    │   └── NINJAV_S001_S001_T033.mp4
    └── FAE_20231026_002
        ├── NINJAV_S001_S001_T003.mp4
        └── NINJAV_S001_S001_T021.mp4
```
