# make symlinks to compressed files of a given list
for i in `./bash_convert.py liste /media/bruno/Elements/h265/ --keep_path_elements=3 --only-print-new-names`; do
    dir=`echo "$i" | awk -F'/' '{print $(NF-2)"/"$(NF-1)}'`;
    dest_dir=$PWD/liens_vers_rushs/$dir;
    mkdir -p $dest_dir;
    ln -s "$i" $dest_dir;
done
