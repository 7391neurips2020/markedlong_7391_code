# Code for Paper ID 7391 (dataset generation)

In this repository, we host the code used to generate our MarkedLong dataset.

Script required to regenerate MarkedLong dataset: `bash marklong_job_runner.sh`

The dataset was generated on a slurm compute cluster in parallel.

File descriptions:

- marklong_job_runner.sh -- Master script that starts multiple jobs for creating markedlong images

- marklong_job -- Calls slurm job for generating markedlong positive images
 
- markshort_job -- Calls slurm job for generating markedlong negative images

- generate_marklong_contours.sh -- Bash script that calls a python script with required dataset parameters to generate positive images

- generate_markshort_contours.sh -- Bash script that calls a python script with required dataset parameters to generate negative images

- connected_contour_draw.py -- Python script with code to generate MarkedLong images using the PIL Python package

- random_shape_generator.py -- Utility functions used by connected_contour_draw.py
