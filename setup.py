from setuptools import setup


setup(
    name="openfast-service",
    version="0.0.0",
    py_modules=['app'],
    entry_points='''
    [console_scripts]
    octue-app=app:octue_app
    ''',
    install_requires=[
        "numpy",
        "octue>=0.2.8",
    ]
)
