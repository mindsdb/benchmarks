import os
import time
import importlib
import subprocess
import numpy as np
from benchmarks import BATCH_ID
from benchmarks.helpers.db import get_mysql
from packaging import version


class BaseFramework():
    def name(self):
        raise NotImplementedError

    def _run_cache(self, ds):
        return None

    def _run(self, ds, df_train, df_test, **kwargs):
        raise NotImplementedError

    def run(self, ds, df_train, df_test, use_cache=True, **kwargs):
        if use_cache:
            cached_row = self._run_cache(ds)
        else:
            cached_row = None

        if cached_row is not None:
            print('using cached result ({} | {} | {})'.format(
                self.name(),
                ds['name'],
                ds['accuracy_function'].__name__
            ))
            return cached_row

        print('Running dataset "{}" with framework "{}"'.format(
            ds['name'],
            self.name()
        ))

        t_0 = time.time()
        result = self._run(ds, df_train, df_test, **kwargs)
        result['runtime'] = time.time() - t_0

        try:
            if np.isnan(float(result['accuracy'])):
                result['accuracy'] = 0
        except Exception as e:
            print(e)
            print('[INFO] Malformed accuracy: {}'.format(result['accuracy']))
            result['accuracy'] = 0

        result['batch_id'] = BATCH_ID
        result['accuracy_function'] = ds['accuracy_function'].__name__
        result['dataset'] = ds['name']

        return result

    def _get_groups(self, group_columns, x_column, y_column, table, sort_fn=lambda r: version.parse, sort_columns=None, not_null_columns=None, extra_columns=None, filter_on=None):
        if extra_columns is None:
            extra_columns = []
        # assert x_column in group_columns
        assert y_column not in group_columns
        assert x_column != y_column
        if sort_columns is None:
            sort_columns = [x_column]

        SELECT = set(['MAX(ran_at)', y_column, *group_columns, *sort_columns, *extra_columns])

        filters = []
        if filter_on is not None:
            for col, val in filter_on.items():
                if isinstance(val, str):
                    val = f"'{val}'"
                filters.append(f'{col} = {val}')

        WHERE = '1' if not_null_columns is None else ' AND '.join('{} IS NOT NULL'.format(column) for column in not_null_columns)
        if len(filters) > 0:
            WHERE += ' AND ' + ' AND '.join(filters)

        # TODO add WHERE use_for_stats = 1
        q = 'SELECT {} FROM {} WHERE 1 AND {} GROUP BY {}'.format(
            ', '.join(SELECT),
            table,
            WHERE,
            ', '.join(group_columns + extra_columns)
        )

        con, cur, cfg = get_mysql('read')
        print(q)
        cur.execute(q)
        rows = cur.fetchall()
        rows = [dict((k, v) for k, v in zip(SELECT, row)) for row in rows]
    
        # group records by (dataset, accuracy_function)
        groups = {}
        for r in rows:
            g = tuple(r[column] for column in group_columns if column != x_column)

            if g not in groups:
                groups[g] = []

            groups[g].append(r)
        
        if sort_fn is not None:
            for g in groups:
                groups[g] = list(sorted(
                    groups[g],
                    key=lambda r: tuple(sort_fn(column) for column in sort_columns)
                ))
        
        return groups

    def get_accuracy_groups():
        raise NotImplementedError

    def get_runtime_groups():
        raise NotImplementedError


class Framework_lightwood(BaseFramework):
    def name(self):
        return 'lightwood'

    def get_accuracy_groups(self, filter_on=None):
        group_by = ['dataset', 'accuracy_function', 'lightwood_version']
            
        return super()._get_groups(
            group_columns=group_by,
            x_column='lightwood_version',
            y_column='accuracy',
            table='benchmarks.v4',
            sort_fn=version.parse,
            sort_columns=['lightwood_version', 'lightwood_commit'],
            extra_columns=['is_dev', 'ran_at'],
            filter_on=filter_on
        )

    def get_confidence_groups(self, filter_on=None):
        return super()._get_groups(
            group_columns=['dataset', 'confidence_accuracy_function', 'lightwood_version'],
            x_column='lightwood_version',
            y_column='confidence_accuracy',
            table='benchmarks.mindsdb',
            sort_fn=version.parse,
            sort_columns=['lightwood_version', 'lightwood_commit'],
            not_null_columns=['confidence_accuracy', 'confidence_accuracy_function'],
            extra_columns=['is_dev', 'ran_at'],
            filter_on=filter_on
        )

    def get_runtime_groups(self, filter_on=None):
        return super()._get_groups(
            group_columns=['dataset', 'accuracy_function', 'lightwood_version'],
            x_column='lightwood_version',
            y_column='runtime',
            table='benchmarks.mindsdb',
            sort_fn=version.parse,
            sort_columns=['lightwood_version', 'lightwood_commit'],
            extra_columns=['is_dev', 'ran_at'],
            filter_on=filter_on
        )