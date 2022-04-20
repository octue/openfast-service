from setuptools import setup


setup(
    name="openfast-service",
    version="0.2.0",
    py_modules=["app"],
    install_requires=[
        "octue @ https://github.com/octue/octue-sdk-python/archive/fix/miscellaneous-fixes.zip",
    ],
)
