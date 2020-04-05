#!/bin/bash

echo 'Attempting to update dataset'
python ./update_covid_numbers.py &&
echo 'Dataset updated'
kaggle datasets version -p ./prod/ -m "updates COVID19 numbers on "