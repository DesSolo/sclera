import os
from subprocess import call, PIPE

base_path = '/tmp'
files = ['config.conf', 'core.py', 'main.py', 'sclera_cli.py']


def create_folders():
    try:
        [os.mkdir(os.path.join(base_path, pth)) for pth in ['backend', 'backend/sclera']]
    except FileExistsError:
        print('Paths exists, skipping...')


def wget_files():
    cmd = lambda x: call(f'wget -P {base_path}/backend/sclera {x}', shell=True, stderr=PIPE)
    base_url = 'https://raw.githubusercontent.com/DesSolo/sclera/master/'
    files = ['config.conf', 'core.py', 'main.py', 'sclera_cli.py']
    [cmd(base_url + file) for file in files]


if __name__ == '__main__':
    # create_folders()
    wget_files()
