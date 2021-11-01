import json
from flask import Flask, render_template, redirect
from flask.globals import g
import numpy as np
from benchmarks.frameworks import Framework_lightwood
from flask import request
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/accuracy_plots')


def make_ul(heading, arr):
    return f'''
    <br>
    <h4>{heading.capitalize()}</h4>
    <ul><li>
    {'</li><li>'.join(arr)}
    </li></ul>
    '''


def get_local_group():
    group = {}
    try:
        with open('REPORT.db', 'r') as fp:
            for line in fp.readlines():
                obj = json.loads(line)
                obj['ran_at'] = datetime.datetime.now()
                group[(obj['dataset'], obj['accuracy_function'])] = [obj]
    except Exception:
        pass
    return group


@app.route('/compare/<first>/<second>')
def compare(first, second):
    # @TODO Add special "stable" case for comparing against the best accuracies across all of lightwood
    multiversion = False
    last = None
    if first == 'best_of_all_time':
        multiversion = True
        first_group = Framework_lightwood().get_accuracy_groups(filter_on={'is_dev': False})
    elif first.startswith('last_'):
        multiversion = True
        last = int(first.replace('last_', ''))
        first_group = Framework_lightwood().get_accuracy_groups(filter_on={'is_dev': False})
    elif len(first.split('.')) == 3:
        first_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_version': first, 'is_dev': False})
    else:
        first_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_commit': first})

    if second == 'local':
        second_group = get_local_group()
    elif len(second.split('.')) == 3:
        second_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_version': second, 'is_dev': False})
    else:
        second_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_commit': second})

    if len(second_group) == 0:
        return 'Missing'

    first_group_dict = {}
    second_group_dict = {}

    dct = {}
    for (ds, af), res in first_group.items():
        if ds not in dct:
            dct[ds] = {}
        if last is not None:
            dct[ds][af] = sorted(res, key=vers_sort)[-last:]
        else:
            dct[ds][af] = res

    for ds in dct:
        for af in dct[ds]:
            max_res = 0
            for r in dct[ds][af]:
                if multiversion and r['lightwood_version'] == 'Native 2.48.0':
                    continue
                if r['lightwood_version'] != second and r['lightwood_commit'] != second:
                    if r['accuracy'] > max_res:
                        max_res = r['accuracy']
                        first_group_dict[(ds, af)] = r

    for (ds, af), res in second_group.items():
        second_group_dict[(ds, af)] = res[0]

    missing = []
    equal = []
    worst = []
    better = []
    dataset_print_dict = {}

    total_improvement = 0
    relative_total_improvement = 0
    for (ds, af) in first_group_dict:
        first_acc = first_group_dict[(ds, af)]['accuracy']
        second_acc = second_group_dict.get((ds, af), {'accuracy': None})['accuracy']

        ds_str = f'Dataset: {ds} with accuracy function {af}'
        if second_acc is None:
            missing.append(ds_str)
            improv = None
        else:
            
            if first_acc <= 0:
                if second_acc > first_acc:
                    relative_improv = 1
                else:
                    relative_improv = 0
            else:
                relative_improv = (second_acc - first_acc) / first_acc
            
            relative_total_improvement += relative_improv
               
            if first_acc < 1 and second_acc < 1:
                improv = max(second_acc, 0) - max(first_acc, 0)
                print(f'Improvement of {round(improv*100,2)}% (out of the max accuracy) for {ds}')
            else:
                print(f'Accuracy function for {ds} doesn\'t support improvement calculation')
                improv = 0
                    
            total_improvement += improv
            if np.abs(improv) < 0.02:
                equal.append(ds_str)
            elif second_acc > first_acc:
                better.append(ds_str)
            elif second_acc < first_acc:
                worst.append(ds_str)
            else:
                raise Exception(f'Something wrong for accuracies {first_acc}, {second_acc}')

        if ds not in dataset_print_dict:
            dataset_print_dict[ds] = []

        first_acc_rnd = round(first_acc, 4)

        if second_acc is None:
            second_acc_rnd = 'Missing'
        else:
            second_acc_rnd = round(second_acc, 4)

        if improv is None:
            improv_rnd = 'Missing'
        else:
            improv_rnd = round(improv, 4)

        dataset_print_dict[ds].append(f'Accuracy function {af} | Before: {first_acc_rnd} | Now: {second_acc_rnd} | Improvement: {improv_rnd}')

    total_improvement = 100 * (total_improvement / (len(worst) + len(better) + len(equal)))
    total_improvement = round(total_improvement, 2)

    relative_total_improvement = 100 * (relative_total_improvement / (len(worst) + len(better) + len(equal)))
    relative_total_improvement = round(relative_total_improvement, 2)

    release_condition = 'relative_total_improvement >= -5 and total_improvement >= -1 and len(missing) == 0'

    if eval(release_condition):
        release = 'Yes'
        release_reason = 'Accuracy is good enough and no datasets are missing'
    elif len(missing) > 0:
        release = 'No'
        release_reason = f' A total of {len(missing)} (datasets, accuracy function) tuples are missing'
    else:
        release = ' No'
        release_reason = 'Aggregate accuracy is too low'

    if request.args.get('release_only', False):
        return release
    else:
        return f"""
            <h1>Aggregate performance</h1>
            <p>Absolute improvement: {total_improvement}%</p>
            <p>Relative improvement: {relative_total_improvement}%</p>
            <p>Should we releases this commit? {release}. Why? {release_reason}</p>
            <p>A total of {len(missing)} datasets are missing</p>
            <p>A total of {len(better)} datasets are performing better</p>
            <p>A total of {len(worst)} datasets are performing worst</p>
            <p>A total of {len(equal)} datasets are about the same</p>
            <br>


            <h2>Per dataset performance<h2>
            {make_ul('Missing', missing)}
            {make_ul('Equal', equal)}
            {make_ul('Better', better)}
            {make_ul('Worst', worst)}
            {''.join([make_ul(ds, dataset_print_dict[ds]) for ds in dataset_print_dict])}
            <br>

            
            <h2>Reading the numbers</h2>
            <p>All comparisons are done between the second commit-hash/version relative to the first</p>
            <p>If the first item being compared is the string "best" this takes the best accuracy from all accuracies of all production runs of the benchmarks (which should be all lightwood release currently on pypi)</p>
            <p>Absolute improvement is calculated as <code>Mean over all (datasource, accuracy) tuples of accuracy_second(datasource, accuracy) - accuracy_first(datasource, accuracy)</code> time 100 (to turn it into % points)</p>
            <p>Relative improvement is calculated as <code>Mean over all (datasource, accuracy) tuples of (accuracy_second(datasource, accuracy) - accuracy_first(datasource, accuracy)) / accuracy_first(datasource, accuracy)</code> time 100 (to turn it into % points)</p>
            <p>Release condition is: {release_condition} (Release is "Yes" if it evaluates to True)</p>
            
        """


def vers_sort(item):
    if 'Native' in item['lightwood_version']:
        return -10

    return int(item['lightwood_version'].replace('.', '')) * pow(10, 12) + item['ran_at'].timestamp()


@app.route('/accuracy_plots')
def accuracy_plots():
    groups = Framework_lightwood().get_accuracy_groups(filter_on={'is_dev': False})
    local_groups = get_local_group()
    for tup in groups:
        if tup in local_groups:
            groups[tup] += local_groups[tup]

    dct = {}
    for ds in list(set(g[0] for g in groups)):
        dct[ds] = {}

    for (ds, af), res in groups.items():
        dct[ds][af] = sorted(res, key=vers_sort)

        for i in range(len(dct[ds][af])):
            dct[ds][af][i]['version_and_commit'] = dct[ds][af][i]['lightwood_version'] + ' - ' + dct[ds][af][i]['lightwood_commit'][:7]

    return render_template(
        'index.html',
        datasets=dct,
        x_axis_key='version_and_commit',
        y_axis_key='accuracy',
    )


if __name__ == '__main__':
    app.run(port=9107, host='0.0.0.0', debug=True)
