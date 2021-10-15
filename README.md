`WARNING: We are currently *not* accepting public PRs with datasets until we have a better quality and rights reviews process in place, ideally automated. Please avoid making pull requests to this repository.`

# Mindsdb Benchmark Suite

Note: This suite is now available to the public but it is still meant to run internally. We will provide local setup instructions, as well as the database mirror needed to compare your results against our ongoing benchmarks very soon.

## Running the benchmarks locally

In order to run the benchmarks locally to check if a change you made to lightwood is positive:

1. Clone this repository and add it to your `PYTHONPATH` and install `requirements.txt` and `ploting/requirements.txt`

2. cd into it and run `python3 benchmarks/run.py --use_db=0 --use_ray=0 --lightwood=#env` | Set `use_ray` to `1` if you have more than 1 GPU or a very good GPU (e.g. a Quadro) | If you wish to benchmark fewer datasets set the `--dataset` argument to the comma separated list of these datasets, e.g. `--datasets=hdi,home_rentals,openml_transfusion`.

3. Once the benchmarks are done running they will generate a preliminary report (`REPORT.md`) and a local file with the full results (`REPORT.db`). These will be used for the plots and reports in the next step

4. Run `python3 ploting/server.py`

5. Got to `http://localhost:9107/compare/best/local` in order to compare performance between your local version and the "best" versions we have in lightwood, you can replace `best` with a specific version or commit hash if you're only interested in that. Go to `http://localhost:9107/accuracy_plots` in order to see accuracy plots that include your local results (they will always be the last data-point on each plot)


http://localhost:9107/compare/best/local

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

