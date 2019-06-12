#!/bin/bash

echo ",,Timing data,," > excel_data.csv
echo ",nan, -p,-s -p, -s" >> excel_data.csv

binary=(binary)
tf=(tf)
tfidf=(tfidf)

for z in $(ls eval_ir);
do
	time_val=$(cat eval_ir/$z | head -n 1| cut -d : -f 2 | tr -d ' ')
	config_type=$(echo $z | cut -d _ -f 2- | sed 's/.txt//g')

	weighting_type=$(echo $z| cut -d _ -f 1)

	if [ $weighting_type == "binary" ]; then
		binary+=(,$time_val)
	elif [ $weighting_type == "tf" ]; then
		tf+=(,$time_val)
	elif [ $weighting_type == "tfidf" ]; then
		tfidf+=(,$time_val)
	fi
	
done

echo $(printf "%s" ${binary[@]}) >> excel_data.csv
echo $(printf "%s" ${tf[@]}) >> excel_data.csv
echo $(printf "%s" ${tfidf[@]}) >> excel_data.csv

echo "" >> excel_data.csv

echo ",,Precision data,," >> excel_data.csv
echo ",nan,-p,-s -p, -s" >> excel_data.csv

binary=(binary)
tf=(tf)
tfidf=(tfidf)

for z in $(ls eval_ir);
do
	time_val=$(cat eval_ir/$z | grep Precision | cut -d : -f 2 | tr -d ' ')
	config_type=$(echo $z | cut -d _ -f 2- | sed 's/.txt//g')

	weighting_type=$(echo $z| cut -d _ -f 1)

	if [ $weighting_type == "binary" ]; then
		binary+=(,$time_val)
	elif [ $weighting_type == "tf" ]; then
		tf+=(,$time_val)
	elif [ $weighting_type == "tfidf" ]; then
		tfidf+=(,$time_val)
	fi
	
done

echo $(printf "%s" ${binary[@]}) >> excel_data.csv
echo $(printf "%s" ${tf[@]}) >> excel_data.csv
echo $(printf "%s" ${tfidf[@]}) >> excel_data.csv

echo "" >> excel_data.csv

echo ",,Recall data,," >> excel_data.csv
echo ",nan,-p,-s -p, -s" >> excel_data.csv

binary=(binary)
tf=(tf)
tfidf=(tfidf)

for z in $(ls eval_ir);
do
	time_val=$(cat eval_ir/$z | grep Recall| cut -d : -f 2 | tr -d ' ')
	config_type=$(echo $z | cut -d _ -f 2- | sed 's/.txt//g')

	weighting_type=$(echo $z| cut -d _ -f 1)

	if [ $weighting_type == "binary" ]; then
		binary+=(,$time_val)
	elif [ $weighting_type == "tf" ]; then
		tf+=(,$time_val)
	elif [ $weighting_type == "tfidf" ]; then
		tfidf+=(,$time_val)
	fi
	
done

echo $(printf "%s" ${binary[@]}) >> excel_data.csv
echo $(printf "%s" ${tf[@]}) >> excel_data.csv
echo $(printf "%s" ${tfidf[@]}) >> excel_data.csv

echo "" >> excel_data.csv

echo ",,F-Measure data,," >> excel_data.csv
echo ",nan,-p,-s -p, -s" >> excel_data.csv

binary=(binary)
tf=(tf)
tfidf=(tfidf)

for z in $(ls eval_ir);
do
	time_val=$(cat eval_ir/$z | grep F-measure| cut -d : -f 2 | tr -d ' ')
	config_type=$(echo $z | cut -d _ -f 2- | sed 's/.txt//g')

	weighting_type=$(echo $z| cut -d _ -f 1)

	if [ $weighting_type == "binary" ]; then
		binary+=(,$time_val)
	elif [ $weighting_type == "tf" ]; then
		tf+=(,$time_val)
	elif [ $weighting_type == "tfidf" ]; then
		tfidf+=(,$time_val)
	fi
	
done

echo $(printf "%s" ${binary[@]}) >> excel_data.csv
echo $(printf "%s" ${tf[@]}) >> excel_data.csv
echo $(printf "%s" ${tfidf[@]}) >> excel_data.csv

echo "" >> excel_data.csv

