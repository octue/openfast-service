from setuptools import setup


setup(
    name="openfast-service",
    version="0.3.1",
    author="Marcus Lugg <marcus@octue.com>",
    py_modules=["app"],
    install_requires=[
        "git+https://github.com/octue/octue-sdk-python.git@better-support-asynchronous-questions",
    ],
)
