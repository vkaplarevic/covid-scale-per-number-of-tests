#! env bash
#cat owid-covid-data.csv | head -1

# get elements for the given country code in the temp file 
cat owid-covid-data.csv | grep $1 > tmp.csv

# pass the file to the python script
python3 ./graph-resize.py ./tmp.csv $1 max

# remove the temp file.
rm ./tmp.csv

