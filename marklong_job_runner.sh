#!/bin/bash
for i in {1..10}
do
	sbatch -p general_short ./marklong_job 18 10000
	sbatch -p general_short ./markshort_job 18 10000
	sbatch -p general_short ./marklong_job 18 10000
	sbatch -p general_short ./markshort_job 18 10000
done
