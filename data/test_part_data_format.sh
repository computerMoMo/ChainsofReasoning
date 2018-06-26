#!/usr/bin/env bash
data_set=("test_part_2")
int2torch="th int2torch.lua"
movie_out_dir="movie_output_data/rate"
for set in "${data_set[@]}"
do
	echo $set
	dataDir=${movie_out_dir}/${set}
	dataset=$set
	if [ -f ${movie_out_dir}/${dataset}.list ]; then
		rm ${movie_out_dir}/${dataset}.list #the downstream training code reads in this list of filenames of the data files, split by length
	fi
	echo "converting $dataset to torch files"
	for ff in $dataDir/*.int
	do
	    echo $ff
		out=`echo $ff | sed 's|.int$||'`.torch
		$int2torch -input $ff -output $out -tokenLabels 0 -tokenFeatures 1 -addOne 1 #convert to torch format
		if [ $? -ne 0 ]
		then
			echo 'int2torch failed!'
			echo 'Failed for relation'
			continue #continue to the next one
		fi
	done
done


for set in "${data_set[@]}"
do
	echo $set
	dataDir=${movie_out_dir}/${set}
	for f in `ls $dataDir/*.torch`
	do
		cmd="th insertClassLabels.lua -input $f -classLabel 1"
		$cmd
	done
done