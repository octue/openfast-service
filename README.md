# openfast-service
A simple wrapper around OpenFAST to run it as a cloud service. This repository is mirrored to Google Cloud Source Repositories.

## OpenFAST
OpenFAST Docs: https://openfast.readthedocs.io
### OpenFAST compiled executable
Can be compiled from source: https://github.com/OpenFAST/OpenFAST
or installed from conda forge:
`conda install -c conda-forge openfast`

### Regression Tests
Regression tests are currently at:
https://github.com/OpenFAST/r-test

**Controller DLLs:**

Before running some tests, the controller DLL should be compiled for your system. 
DISCON controller comes with source code and makefiles. 
To build DISCON on the LINUX system use:

```
cmake DISCON
make
```

### OpenFAST Models of the wind turbines:
NREL Wind Turbine Models can be found at:
https://github.com/NREL/openfast-turbine-models/


### OpenFAST Tools
https://github.com/OpenFAST/python-toolbox

## Wrapper Documentation

The docs are built automatically, and hosted at:
https://windenergie-hsr.gitlab.io/aerosense/digital-twin/fsi-twins/openfast-service/

### Building documents manually

**If you did need to build the documentation**

Install `doxgen`. On a mac, that's `brew install doxygen`; other systems may differ.

Install sphinx and other requirements for building the docs:
```
pip install -r docs/requirements.txt
```

Run the build process:
```
sphinx-build -b html docs/source docs/build
```
