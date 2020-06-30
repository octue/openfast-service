# panel-code-twine-python
A simple twine that runs panel codes

## Creating a twine

First, think about:
- what data you want to flow into and out of the app
- what kinds of datasets (groups of files) the app might need to access
- what other applicaitons / twins ('children') you need to use
- what credentials you might need (e.g. if you're accessing a database or a third party API

The **twine** file secifies all these things and more. First, place an empty `twine.json` file in the root directory of the app.

See [https://twined.readthedocs.io](https://twined.readthedocs.io) for everything there is to know about how to define a twine. If you log in to [octue.com](https://www.octue.com/login) you'll find tools to help you build the twine.

*Note: this example app is not up to date with the current version of twined! Follow or comment on [this issue](https://github.com/octue/octue-app-python/issues/1).*

 
## First steps in development

If you've not developed python applications before, we strongly recommend the following practices:

- Use an Integrated Development Environment (IDE) to help you. We recommend [Pycharm, by Jetbrains](https://www.jetbrains.com/pycharm/) because it's cross-platform (i.e. for Windows, Mac and Linux), very friendly, and there's a free "Community Edition" which should have all the features you need for now.
- Ensure Python 3.5 or greater is installed. (Mac users: use [pyenv](https://github.com/pyenv/pyenv), windows users could try [pyenv-win](https://github.com/pyenv-win/pyenv-win)) 
- [Configure a Virtual Environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) to ensure you always have a consistent python environment and packages installed.

Once you've set yourself up with Python 3.7+, an IDE and an activated virtual environment, you're ready to go:

- PyCharm will usually do this for you, but if not, install the project dependencies (see `requirements.txt`).
- Set up a directory containing your input data. How to do this is covered below, in 'Data Directories'.

### Running your app (whilst developing)

`>> python app.py`. Simple as that. You can specify a 

 
### Connecting to the octue platform

 1. Log in to [octue.com](www.octue.com), click `applications > create` in the sidebar, and follow the wizard. Simples!
 

## Data directories

Octue uses a strict folder structure, to help separate input, output, and temporary data. The structure looks like this:
```
my_data_folder
    |
    |- input
    |    |
    |    |- config.json
    |    |- manifest.json
    |    |- <dataset_xx>
    |    |    |
    |    |    |- <file_xxx>
    |    |    |- <file_xxy>
    |    |    |- <file_xxz>
    |    |    |- ...
    |    | 
    |    |- <dataset_xy>
    |    |    |
    |    |    |- <file_xyx>
    |    |    |- <file_xyy>
    |    |    |- <file_xyz>
    |    |    |- ...
    |    |
    |    |- ...
    |
    |- logs
    |    |
    |    |- ...
    |
    |- tmp
    |    |
    |    |- ...
    |
    |- output
    |    |
    |    |- ...
```

- Folder **`input`** contains any input datasets (groups of files). Within each dataset - you can simply dump a load of files created by an instrument or supplied by a third party here. These files should never be altered by the application.
- Folder **`logs`** will contain log files produced while running the application. You shouldn't need to use these, as all output will be shown either in your terminal or on octue online.
- Folder **`tmp`** you can write any temporary files (e.g. large cached calculations that are reused but don't form part of the results) here.
- Folder **`output`** all output files should be saved to this directory. Any output files (like figures) produced by octue are saved here too.

- File **``input/manifest.json``** contains a list of all the files in the input directory, with any tags that are applied (see 'generating the manifest file', below)..
- File **``input/config.json``** contains a list of options and configuration parameters to use when running the application (see 'generating the config file', below).


### Generating the config and manifest files

When a user (you, or someone else) launches an application on octue, they fill in a form (which is generated from the twine). That creates a
`config.json` file automatically. You can download this for local development.

Connecting datasets to the application creates the `manifest.json`, which you can download too.

But, if you're just testing your own application out, its helpful to generate these files yourself.

The `octue_app_python` repository contains a `schema.json` for the example application. 
Go to [the octue schema playground](https://www.octue.com/schema/playground), and paste the entire contents of 
`schema.json` into the top left box.

Fill in the form (it's already populated with defaults) and you'll see your **config** change as you do, in the bottom
right box. This is what gets pasted into `config.json` (see `octue_app_python/example_data/config.json`). 

You can play around with schema in that playground (if you're having trouble, use the excellent 
[JSON Editor Online](https://jsoneditoronline.org/) to help debug them if you run into trouble.
