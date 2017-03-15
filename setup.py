# !/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path

from setuptools import find_packages
from setuptools import setup

"""

"""

__version__ = (0, 0, 2)
here = path.abspath(path.dirname(__file__))
license = 'MIT'

try:
    long_description = open(path.join(here, 'README.rst'), encoding='utf-8').read()
except:
    long_description = ''

setup(
    name='bta',
    version=".".join(str(x) for x in __version__),
    description='ZZiZiLY bta Project',
    long_description=long_description,
    url='https://github.com/deuxksy/bta',
    author='SeokYoung Kim',
    author_email='crom@zzizily.com',
    license=license,
    test_suite='tests',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # 프로젝트 상태 (성숙도)
        'Development Status :: 2 - Pre-Alpha',
        # 누구를 위한
        'Intended Audience :: Developers',
        # 어떤것을 위한
        'Topic :: Software Development :: Commons Library',
        # 라이센스선택 (위의 license 와 동일해야 함)
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Korean',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='zzizily bta apps',
    # my_module.py 만 배포하려면
    # py_modules = [ 'my_module'],
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'redis',
        'requests',
        'scrapy',
        'pip-review',
    ],
    # package 필요한 데이터 파일 Python 2.6 이하를 사용한다면 MANIFEST.in 포함 해야합니다.
    # package_data={
    #     'bta': [
    #         'resources/local_config.ini',
    #         'resources/dev_config.ini',
    #         'resources/prod_config.ini',
    #     ],
    # },
    # 'package_data'가 선호되는 접근 방식이지만 어떤 경우에는 데이터 파일을 패키지 외부에 배치해야합니다.
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # 이 경우 'data_file'이 '<sys.prefix> / my_data'에 설치됩니다.
    # data_files=[(' my_data ', [' data / data_file '])],
    # scripts=[
    #     'scripts/init.cmd',
    #     'scripts/run.cmd',
    #     'scripts/destroy.cmd',
    #     'scripts/start.cmd',
    # ]
)
