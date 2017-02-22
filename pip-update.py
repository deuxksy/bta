"""
python package update 하기
"""

import pip
from subprocess import call

for dist in pip.get_installed_distributions():
    call('pip install --upgrade {app}'.format(app=dist.project_name), shell=True)