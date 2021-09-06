import inspect
from types import FunctionType
from typing import List, Optional, Union
import os


class DatasetInterface():
    tags: List[str]
    file: str
    active: bool
    accuracy_functions: List[FunctionType]
    target: str
    learn_kwargs: object
    num_folds: int
    strict_mode: bool = True
    source: Union[None, str] = None
    sota_accuracy: Union[None, float] = None
    is_open_license: bool = None
    license: str = None
    name: Optional[str] = None

    def validate(self):
        errors = []

        optional = set(['strict_mode', 'sota_accuracy', 'name'])
        required = set(inspect.getmembers(DatasetInterface)[0][1].keys()) - optional
        present = set(inspect.getmembers(type(self))[3][1].keys()) - set(['__module__', '__doc__'])

        for field in present:
            if field not in required | optional:
                errors.append(f'Unkown field: {field}')
        
        for field in required:
            if field not in present:
                errors.append(f'Missing required field: {field}')
        
        for tag in self.tags:
            if tag not in ['classification', 'regression', 'text', 'timeseries']:
                errors.append(f'Unkown tag: {tag}')
        if len(errors) > 0:
            exp = f'Got the following errors for {self.name}:\n*' + '\n*'.join(errors) + '\n---------------------\n'
            raise Exception(exp)
    
    def __init__(self, dataset_dir, ds_name):
        self.name = ds_name
        self.validate()
        ds_path = os.path.join(dataset_dir, self.name)
        self.file = os.path.join(dataset_dir, self.name, self.file)
        if not os.path.exists(self.file):
            os.system(f'cd {ds_path} && yes | unzip {self.file}.zip')
        
