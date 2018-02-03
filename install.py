import os
from subprocess import call, PIPE

base_path = '/tmp'
files = ['config.conf', 'core.py', 'main.py', 'sclera_cli.py', 'sclera.service']


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


def add_service():
    os.rename(f'{base_path}/backend/sclera/sclera.service', '/etc/systemd/system/multi-user.target.wants/sclera.service')


if __name__ == '__main__':
    print('Only for root!')
    create_folders()
    wget_files()
    add_service()