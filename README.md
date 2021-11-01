# Mindsdb Benchmark Suite

This is a benchmark suite meant for automatic machine learning frameworks, containing a broad range of datasets and accuracy functions to evaluate performance on them. You can see an up to date list of all datasets and accuracy functions, as well as ongoing lightwood performance at: [http://benchmarks.mindsdb.com:9107/accuracy_plots](http://benchmarks.mindsdb.com:9107/accuracy_plots)

## Running the benchmarks (open source user)

In order to run the benchmarks locally to check if a change you made to lightwood is positive:

0. Install pip, git and git-lfs (note: when you pull new changes you have to `git lfs pull` in addition to `git pull` *and* you have add large files to `git-lfs` instead of it)

1. Clone this repository and add it to your `PYTHONPATH` and install `requirements.txt` and `ploting/requirements.txt`

2. cd into it and run `python3 benchmarks/run.py --use_db=0 --use_ray=0 --lightwood=#env` | Set `use_ray` to `1` if you have more than 1 GPU or a very good GPU (e.g. a Quadro) | If you wish to benchmark fewer datasets set the `--dataset` argument to the comma separated list of these datasets, e.g. `--datasets=hdi,home_rentals,openml_transfusion`.

3. Once the benchmarks are done running they will generate a preliminary report (`REPORT.md`) and a local file with the full results (`REPORT.db`). These will be used for the plots and reports in the next step

4. Run `python3 ploting/server.py`

5. Got to `http://localhost:9107/compare/best_of_all_time/local` or `http://localhost:9107/compare/last_{x}/local`. `best_of_all_times` choses the best version of lightwood for each databaset+accuracy function combination, while `last_{x}` looks at the last `x` versions. We usually like comparing with `last_3` to determine if we should release a new version. You can also compare with a specific version or commit hash if you're only interested in that. Go to `http://localhost:9107/accuracy_plots` in order to see accuracy plots that include your local results (they will always be the last data-point on each plot)

## Running the benchmarks (lightwood researcher or colaborator)

Same as above, but you should have access to a `db_info.json` file and thus be able to run with `--use_db=1` to store your results in our database, this means you can compare using urls like `http://benchmarks.mindsdb.com:9107/compare/<some hash>/<hash of your branch>` for easier sharing and to appease automatic release scripts.

### Release protocol

When a PR is made into stable you should chose a machine (ideally the benchmarking rig on ec2) and:
1. Clone the latest commit being merged (let's say commit hash for this is `foobar`)
2. Run the benchmarks via `python3 benchmarks/run.py --use_db=1 --use_ray=1 --lightwood=#env`
3. Check `http://benchmarks.mindsdb.com:9107/compare/last_3/foobar` in order to see if a release can be made (be patient, it might take 3-5 hours for all benchmarks to run)
4. Re-run github actions for the latest commit (excluding the documentation bot's commits) and make sure all is green
5. Once we release a new stable run benchmarks for it using `--is_dev=0` such that it gets added to the official list of released versions