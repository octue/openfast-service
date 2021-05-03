import os
from setuptools import setup


def git_version():
    return os.system('git rev-parse HEAD')


setup(
    name="panel-codes-twine",
    version=git_version(),
    py_modules=['app'],
    entry_points='''
    [console_scripts]
    octue-app=app:octue_app
    ''',
    install_requires=[
        "numpy",
        "octue>=0.1.16",
    ]
)
