
def get_commit():
    import lightwood
    import os
    import subprocess
    dirname = os.path.dirname(lightwood.__file__)
    commit = subprocess.check_output(f'cd {dirname} && cd .. && git rev-parse HEAD', shell=True).decode().strip()
    return commit
