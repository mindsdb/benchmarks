from flask import Flask, render_template, redirect
import numpy as np
from benchmarks.frameworks import Framework_lightwood
from flask import request


app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/accuracy_plots')


@app.route('/compare/<first>/<second>')
def compare(first, second):
    # @TODO Add special "stable" case for comparing against the best accuracies across all of lightwood
    if first == 'best':
        first_group = Framework_lightwood().get_accuracy_groups()
    elif len(first.split('.')) == 3:
        first_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_version': first})
    else:
        first_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_commit': first})

    if len(second.split('.')) == 3:
        second_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_version': second})
    else:
        second_group = Framework_lightwood().get_accuracy_groups(filter_on={'lightwood_commit': second})

    if len(second_group) == 0:
        return 'Missing'

    first_group_dict = {}
    second_group_dict = {}

    for (ds, af), res in first_group.items():
        max_res = 0
        for r in res:
            if first == 'best' and r['lightwood_version'] == 'Native 2.48.0':
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
    total_improvement = 0
    relative_total_improvement = 0
    for (ds, af) in first_group_dict:
        first_acc = first_group_dict[(ds, af)]['accuracy']
        second_acc = second_group_dict.get((ds, af), {'accuracy': None})['accuracy']

        if second_acc is None:
            missing.append((ds, af))
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
            if np.abs(improv) < 0.05:
                equal.append((ds, af))
            elif second_acc > first_acc:
                better.append((ds, af))
            elif second_acc < first_acc:
                worst.append((ds, af))
            else:
                raise Exception(f'Something wrong for accuracyies {first_acc}, {second_acc}')

    total_improvement = 100 * (total_improvement / (len(worst) + len(better) + len(equal)))
    total_improvement = round(total_improvement, 2)

    relative_total_improvement = 100 * (relative_total_improvement / (len(worst) + len(better) + len(equal)))
    relative_total_improvement = round(relative_total_improvement, 2)

    release = ' No'
    if relative_total_improvement >= 0 and total_improvement >= 0 and len(worst) == 0 and len(missing) == 0:
        release = 'Yes'

    if request.args.get('release_only', False):
        return release
    else:
        return f"""
            In short
            <br>
            Total improvement: {total_improvement}% (diff as % of 1 for acc functions capped at 1, scores < 0 ignored)
            <br>
            Relative total improvement: {relative_total_improvement}% as % of first accuracy (marked as 100% if going from a negative to a positive score)
            <br>
            {len(missing)} missing
            <br>
            {len(equal)} equal
            <br>
            {len(worst)} worst
            <br>
            {len(better)} better
            <br>
            Should we releases? ---{release}---
            <br>
            <br>
            Details:
            <br>
            Missing: {missing}
            <br>
            Worst: {worst}
            <br>
            Better: {better}
            <br>
            Equal: {equal}
        """


def vers_sort(item):
    if 'Native' in item['lightwood_version']:
        return -10

    return int(item['lightwood_version'].replace('.', '')) * pow(10, 12) + item['ran_at'].timestamp()

@app.route('/accuracy_plots')
def accuracy_plots():
    groups = Framework_lightwood().get_accuracy_groups()
    print(groups)
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
