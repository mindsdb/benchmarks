import os
import sys
import inspect
import json

import MySQLdb


def get_mysql():
    with open(os.path.dirname(os.path.abspath( os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) )) + '/db_info.json', 'rb') as fp:
        cfg = json.load(fp)

    con = MySQLdb.connect(
        cfg['mysql']['host'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['database']
    )
    cur = con.cursor()
    return con, cur, cfg


def query(query_str):
    con, cur, cfg = get_mysql()
    cur.execute(query_str)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    con.close()
    return rows


def setup_mysql():
    con, cur, cfg = get_mysql()

    shared_schema = """
    id INT NOT NULL AUTO_INCREMENT
    ,ran_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ,batch_id Text
    ,dataset Text
    ,accuracy Float
    ,accuracy_function Text
    ,runtime Float
    """

    schema_mindsdb = """
    ,confidence_accuracy Float
    ,confidence_accuracy_function Text
    ,native_version Text
    ,lightwood_version Text
    """

    cur.execute("""CREATE DATABASE IF NOT EXISTS benchmarks""")

    cur.execute(f"""CREATE TABLE IF NOT EXISTS benchmarks.mindsdb_prod (
        {shared_schema}
        {schema_mindsdb}
        ,PRIMARY KEY(id)
    ) ENGINE=InnoDB""")

    cur.execute(f"""CREATE TABLE IF NOT EXISTS benchmarks.mindsdb_dev(
        {shared_schema}
        {schema_mindsdb}
        ,branch Text
        ,PRIMARY KEY(id)
    ) ENGINE=InnoDB""")

    cur.execute(f"""CREATE TABLE IF NOT EXISTS benchmarks.sklearn (
        {shared_schema}
        ,sklearn_version Text
        ,PRIMARY KEY(id)
    ) ENGINE=InnoDB""")

    cur.execute(f"""CREATE TABLE IF NOT EXISTS benchmarks.pycaret (
        {shared_schema}
        ,sklearn_version Text
        ,PRIMARY KEY(id)
    ) ENGINE=InnoDB""")

    cur.execute(f"""CREATE TABLE IF NOT EXISTS benchmarks.sota (
        {shared_schema}
        ,source Text
        ,PRIMARY KEY(id)
    ) ENGINE=InnoDB""")

    try:
        cur.execute('CREATE INDEX dataset_mindsdb_prod ON benchmarks.mindsdb_prod (dataset(100))')
    except:
        pass

    try:
        cur.execute('CREATE INDEX batch_id_mindsdb_prod ON benchmarks.mindsdb_prod (batch_id(100))')
    except:
        pass


    try:
        cur.execute('CREATE INDEX dataset_mindsdb_dev ON benchmarks.mindsdb_dev (dataset(100))')
    except:
        pass
    try:
        cur.execute('CREATE INDEX batch_id_mindsdb_dev ON benchmarks.mindsdb_dev (batch_id(100))')
    except:
        pass

    try:
        cur.execute('CREATE INDEX dataset_sklearn ON benchmarks.sklearn (dataset(100))')
    except:
        pass
    try:
        cur.execute('CREATE INDEX batch_id_sklearn ON benchmarks.sklearn (batch_id(100))')
    except:
        pass

    try:
        cur.execute('CREATE INDEX dataset_pycaret ON benchmarks.pycaret (dataset(100))')
    except:
        pass
    try:
        cur.execute('CREATE INDEX batch_id_pycaret ON benchmarks.pycaret (batch_id(100))')
    except:
        pass

    try:
        cur.execute('CREATE INDEX dataset_sota ON benchmarks.sota (dataset(100))')
    except:
        pass
    try:
        cur.execute('CREATE INDEX batch_id_sota ON benchmarks.sota (batch_id(100))')
    except:
        pass
