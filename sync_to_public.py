# Create the "public" benchmark repository out of this private one
from typing import List
from benchmarks.datasets.dataset import DatasetInterface
import os
import shutil
import sys
import importlib


private_dir = sys.argv[1]
public_dir = sys.argv[2]

CURRENT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
DATASETS_DIR = os.path.join(CURRENT_DIR, os.path.join('benchmarks', 'datasets'))


ds_list: List[DatasetInterface] = []
for ds_name in os.listdir(DATASETS_DIR):
    if '__' in ds_name or '.py' in ds_name:
        continue
    try:
        info = importlib.import_module(f'benchmarks.datasets.{ds_name}.info')
    except ImportError:
        print('[INFO] Dataset {} doesn\'t contain info.py'.format(ds_name))
        continue

    dataset = info.Dataset(DATASETS_DIR, ds_name)
    ds_list.append(dataset)

public_ds_names = [x.name for x in ds_list if x.is_open_license]
private_ds_names = [x.name for x in ds_list if not x.is_open_license]

for src_dir, dirs, files in os.walk(private_dir):
    dst_dir = src_dir.replace(private_dir, public_dir, 1)

    stop_copy = False
    for ds_name in private_ds_names:
        if ds_name in str(dst_dir):
            print(f'Not copying files belonging to closed dataset {ds_name}')
            stop_copy = True
            break
    if stop_copy:
        continue

    if '.git' in str(dst_dir):
        print(f'Not copying files in git related dir: {dst_dir}')
        continue

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for file_ in files:
        if str(file_) in ('db_info.json', 'RUN.md'):
            print(f'Not copying file {file_}')
            continue

        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)
