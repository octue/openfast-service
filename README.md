# openfast-service
A simple wrapper around OpenFAST to run it as a cloud service.

The docs are built automatically, and hosted at:
https://windenergie-hsr.gitlab.io/aerosense/digital-twin/fsi-twins/openfast-service/

![](https://storage.googleapis.com/static.octue.com/view-of-openfast-service.png)

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


## OpenFAST Service Infrastructure

TODO this should probably go in the docs, chucking it here for now:

### The Question

Initially, we wanted to make the OpenFAST Service as simple as possible for a proof-of-concept.
To do achieve that, we need to decide - what is the question we're trying to answer? We will, of course, evolve the
service from this point, to become a much more general simulator of turbine performance.

**Question 1**
For a given 10 minute period of the Aventa turbine, at the Aventa site, what is the power output and base bending moment?

*Why do we want to know this?*
So that we can compare those results with measured values from the turbine.

**Question 2**
For a given 10 minute period of the Aventa turbine operation, what is the rotor-angle-averaged averaged AoA over that period (for, say 36 angular positions)?

*Why do we want to know this?*
So that for polar inputs which are *not* derived from aerosense measurements, we can compare these outputs with rotor-angle-averaged AoA from the Aerosense system as validation.


### Inputs

#### Input files: Turbine Model Dataset
    - We will have a bucket in the aerosense project for turbine models.
    - Each turbine model has a folder, named sensibly e.g. `aventa-prototype-whatever` which will be the key of our turbine model
    - A turbine model dataset is a collection of files representing a turbine, and will roughly consist of:
        - Aerodynamics file (including specified path to separate folder for aerofoil polars)
        - Blades file
        - Tower file
        - Structural properties files
        - Main input file
        - Controller .so file

#### Input values

A detailed overview of openFAST inputs is available [here](https://openfast.readthedocs.io/en/latest/source/user/aerodyn/input.html#aerodyn-driver-input-file).
We distil most of them into the specific turbine model, but supply some here as the main parameters of the service,
enabling the questions to be asked with varying parameters.

- Inflow wind speed
    - TODO Determine `hub_height` parameter from the input model

- cl, cd polars
   - A polar is a graph, basically, of lift vs drag over a range of alpha (angle of attack)
   - Polars can come from 2d cfd, aerosense measurements, wind tunnel measurements
   - TODO if trying to drive openFAST with polars derived from aerosense, we only have three stations. This won't give a
     robust distribution of polars across the blade. Either we need to robustly interp/extrap within this service, or we
     need to interp/extrap from aerosense results prior to calling openFAST with them.

- Aerosense sensor radii locations for AoA measurement


- Turbulence generator input data

#### Output values
- 10-minute timeseries of Turbine power and thrust coefficients (array of two tuples CP and CT [no units])
- 10-minute timeseries of Tower base bending moments (array of six tuples Fx, Fy, Fz, Mx, My, Mz [N])
- Measurements are sampled at 10/100Hz for 10 minutes, so we should match this dataset in form
- Rotor-angle-averaged AoA at sensor locations (for comparison with AoAs calculated)


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
