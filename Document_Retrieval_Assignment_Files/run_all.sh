#!/bin/bash

for type in "binary" "tf" "tfidf"
do
	echo "$type weighting scheme"
	for config in "-s" "-p" "-s -p" ""
	do
		filename="_nan"
		if [[ $config == "-s" ]]; then
			filename="_stoplist"
		elif [[ $config == "-p" ]]; then
			filename="_stemming"
		elif [[ $config == "-s -p" ]]; then
			filename="_stoplist_stemming"
		fi

		echo "$filename configuration being used.."
		python ir_engine.py $config -w $type -o results/$type$filename.txt > eval_ir/$type$filename.txt 2>&1 
		python eval_ir.py cacm_gold_std.txt results/$type$filename.txt >> eval_ir/$type$filename.txt
	done
	echo ""
done
