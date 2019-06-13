#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
pwd; hostname; date

python3 process.py 201902

python3 doc2vec_jp.py 201902
