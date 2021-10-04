# OpenML AutoML benchmark scripts

This folder has instructions and scripts needed to run the OpenML AutoML benchmark and compare MindsDB results with other AutoML frameworks.

Link to benchmark: https://github.com/openml/automlbenchmark
Link to fork: https://github.com/paxcema/automlbenchmark

## Benchmark Usage

1. Clone the fork for the openml/automlbenchmark repo from https://github.com/paxcema/automlbenchmark
2. Checkout the `mindsdb_integration_v2` branch (note: these steps are temporal, we should PR this branch into the official repo eventually, but the docker integration work is still pending)
3. Create a virtual environment and do `pip install -r requirements.txt` for that repo
4. To install MindsDB: `python3 runbenchmark.py MindsDB -s only`
5. To test it: `python3 runbenchmark.py MindsDB -f 0 -Xtest_mode`
6. To run the benchmark: `python runbenchmark.py MindsDB mdb_custom 1h4c`. The `1h4c` mode runs datasets with 10 different folds, a time budget of 1 hour, and 4 CPU cores.
7. There are additional benchmarks with our current timed out datasets: `mdb_timeouts` and the "large" datasets as classified by OpenML: `large`. To run these: `python runbenchmark.py MindsDB large 1h4c; python runbenchmark.py MindsDB mdb_timeouts 1h4c`.

## Consolidating results
After running a task, a folder will be created in `results/` with the task's name. Coy the `scores/results.csv` file of all relevant tasks to a new directory.

Run `python scripts/consolidate.py path/to/tasks/results` to get a summary of each dataset in all of the processed CSVs in the `consolidated.csv` file.

Run `python scripts/compare.py path/to_consolidated.csv/ path/to_other_frameworks.csv/` to insert MindsDB performance in the matrix of all AutoML frameworks as provided by OpenML (or ran internally, though in practice this would be very time consuming and compute intensive). This script will return CSVs that compare all frameworks in the relevant metrics (AUC, LogLoss, Runtime, Accuracy).

Finally, if you have an older `consolidated.csv` from a previous benchmark run, you can get the % difference between this and the newest results by doing `python scripts/get_openml_improvements.py March2021/consolidated.csv June21/consolidated.csv June21/`.

## Notes
Running all three `mdb_custom mdb_timeouts large` will take about a day and a half (not entirely sure, as I've left it running during the weekends)

## Datasets per split
1. mdb_custom.yaml

amazon_employee_access
apsfailure
australian
bank-marketing
blood-transfusion
car
christine
cnae-9
connect-4
credit-g
dilbert
fabert
fashion-mnist
guiellermo
helena
higgs
jannis
jasmine
jungle_chess_2pcs_raw_endgame_complete
kc1
kddcup09_appetency
kr-vs-kp
mfeat-factors
miniboone
nomao
numerai28.6
phoneme
riccardo
robert
segment
shuttle
sylvine
vehicle
volkert

3. mdb_timeouts.yaml

dilbert
Fashion-MNIST
guillermo
Helena
riccardo
Robert


5. large.yaml

Airlines
Albert
Covertype
Dionis