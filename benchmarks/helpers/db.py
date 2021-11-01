import os
import json
import benchmarks
import MySQLdb


def get_mysql(mode='write'):
    if mode == 'write':
        db_info_path = os.path.join(os.path.dirname(os.path.abspath(benchmarks.__file__)), 'db_info.json')
    else:
        db_info_path = os.path.join(os.path.dirname(os.path.abspath(benchmarks.__file__)), 'public_db_info.json')

    with open(db_info_path, 'rb') as fp:
        cfg = json.load(fp)

    con = MySQLdb.connect(
        cfg['mysql']['host'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['database']
    )
    cur = con.cursor()
    return con, cur, cfg


def setup_mysql():
    con, cur, _ = get_mysql()

    cur.execute(f"""CREATE TABLE IF NOT EXISTS benchmarks.v4 (
        id INT NOT NULL AUTO_INCREMENT
        ,ran_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ,dataset TEXT NOT NULL
        ,accuracy FLOAT NOT NULL
        ,accuracy_function TEXT NOT NULL
        ,runtime FLOAT NOT NULL
        ,lightwood_version TEXT NOT NULL
        ,lightwood_commit TEXT NOT NULL
        ,is_dev BOOL NOT NULL
        ,num_folds INT # When None => CV was not used
        ,accuracy_per_fold TEXT # When None => CV was not used
        ,accuracy_per_mixer TEXT
        ,PRIMARY KEY(id)
    ) ENGINE=InnoDB""")

    con.commit()
    con.close()