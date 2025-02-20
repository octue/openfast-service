# openfast-service
A simple wrapper around [OpenFAST](https://openfast.readthedocs.io) to run it as a Twined data service in the
cloud. Uses the [official OpenFAST docker image architected by Octue](https://github.com/OpenFAST/openfast/pull/2124) as a base image.

## Installation

### Install the client
```shell
pip install octue
```

### Set up the data service

There are two main options:
- Self-hosting - use our open-source tools to spin up an OpenFAST service in your own private cloud:
  - [Twined Terraform module](https://github.com/octue/terraform-octue-twined) to spin up the cloud infrastructure
  - [Octue Twined](https://octue-python-sdk.readthedocs.io/en/latest/) data service framework to trigger OpenFAST
    simulations
- [Octue hosting](https://www.octue.com/consultancy) - we sort everything for you

## Usage
```python
from octue.resources import Child, Dataset, Manifest


# Point to your data service
child = Child(
    id="my-org/openfast-service:0.10.0",
    backend={"name": "GCPPubSubBackend", "project_name": "my-project"},
)

# Upload your input data
dataset = Dataset(path="tests/data/openfast_iea")
dataset.upload(cloud_path="gs://my-bucket/path/to/openfast_dataset")
input_manifest = Manifest(datasets={"openfast": dataset})

# Run the OpenFAST analysis
answer, _ = child.ask(input_manifest=input_manifest, timeout=3600)

# Access the output data
output_dataset = answer["output_manifest"].get_dataset("openfast")
```

## OpenFAST versions

`openfast-service` is versioned separately to OpenFAST. See below for the default version of OpenFAST each version of
the service supports.

| `openfast-service` versions | OpenFAST version |
|-----------------------------| ---------------- |
| `<=0.10.0`                  | `3.5.3`          |
