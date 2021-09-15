from setuptools import setup


setup(
    name="openfast-service",
    version="0.0.0",
    py_modules=['app'],
    install_requires=[
        "octue @ https://github.com/octue/octue-sdk-python/archive/feature/allow-entire-manifest-or-dataset-to-be-downloaded-at-once.zip",
    ]
)
