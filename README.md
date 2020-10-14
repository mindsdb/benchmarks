# MindsDB benchmarks

This repository contains various MindsDB benchmarks. 

## Usage examples

* Run some quick benchmarks locally to check the performance: `python3 run.py --modes=mindsdb_dev --platform=local --speed=fast,medium,slow`
* Compare your local version against sklearn (a naive and an expert implementation): `python3 run.py --modes=sklearn_naive,sklearn_expert,mindsdb_dev  --platform=local --speed=fast,medium,slow`
* Run benchmarks for current stable remotely: `python3 run.py --modes=mindsdb_prod --platform=GCP --speed=fast,medium,slow` [Implementation not done yet]

## Contributions

Before contributing to this repository please make sure that the dataset you are adding are publicly available and can be re-used.

### Adding a dataset

* Add your dataset as a csv in a directory `datasets/{name_of_the_dataset}/data.csv`.
* To specify an accuracy function to evaluate it with and other parameters edit `datasets/{name_of_the_dataset}/info.py`, see [this file as an example](datasets/automobile_insurance/info.py).
* To add an "alternatives" benchmark for the dataset add it to `alternatives/{alternative_name}/{name_of_the_dataset}/benchmark.py`. Currently the supported alternatives are sklearn_expert and sklearn_naive. For an example see [this file](alternatives/sklearn/home_rentals/benchmark.py).

### Issues

If you found any issues with MindsDB when executing the benchmarks, please make sure you report them in the [MindsDB repository](https://github.com/mindsdb/mindsdb).
