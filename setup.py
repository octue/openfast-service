from setuptools import setup


setup(
    name="openfast-service",
    version="0.2.1",
    author="Marcus Lugg <marcus@octue.com>",
    py_modules=["app"],
    install_requires=[
        "coolname>=1.1,<2",
        "octue @ git+https://github.com/octue/octue-sdk-python.git@fix-manifest-bugs",
    ],
)
