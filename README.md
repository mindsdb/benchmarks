# Mindsdb Benchmark Suite

Note: This suite is now available to the public but it is still meant to run internally. We will provide local setup instructions, as well as the database mirror needed to compare your results against our ongoing benchmarks very soon.

## Important

A benchmark is identified by: a dataset name, an accuracy function, a lightwood version, a lightwood commit.
"Running the benchmark" means running all potential dataset and accuracy function combinations for a specific lightwood version and commit.
All benchmarks ran are logged in the database *and* the only way to look at the results will be through the database (plotting server makes this easy)

## Install

As usual: clone, add to python path, install requirements, make sure lightwood is installed. If this doesn't make sense then you shouldn't be running the benchmark suite and instead you should ask for a mindsdb dev environment setup tutorial from a colleague.

## Useful scenarios

### Benchmarking a local experiment

I have a local version / commit-hash / both of lightwood and I want to bench it's accuracy against any other version of lightwood.

Run the benchmarks as: `python3 benchmarks/run.py --lightwood=#env --use_ray=0` (this assume you have a single GPU, if you have multiple GPU or a beasty single GPU use `--use_ray=1`)
Compare as: `http://0.0.0.0:9107/compare/<base lightwood version>/<your version and/or commit hash>`

## Improvement ideas

#### Plotting

2x types of improvement, relative to the previous score *and* relative to total (aka `first - second` for acc score going from 0 to 1). We'll call these "relative" (improvement relative to previous score) and absolute (improvement relative diff on a 0 to 1 scale for accuracy functions that are capped)

For both relative and absolute improvement we'll have:

* Mean
* Median
* Box plot

Also maybe tag datasets as: Classifaction, Regression, Text, Timeseries