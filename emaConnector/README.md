# Vadere EMA Workbench connector
This section holds the in this research build model connector from the [EMA Workbench](https://github.com/quaquel/EMAworkbench) to Vadere. The connector is intended to be included in the EMA Workbench source-code in the future. An instruction on the use of the model connector can be found below.

## Connector configuration
As long as the connector is not yet included in the newest EMA Workbench distribution, the configuration below has to be performed by the user manually. This will become absolute in the near future.

First, get a copy of this repository and locate the `vadere.py` file included in this section. This file serves as the model connector. Secondly, get a copy of the EMA Workbench source code and make sure your Python environment is up-to-date with all the EMA Workbench requirements. 

After all the files are obtained, place the `vadere.py` file inside your EMA Workbench copy under `ema_workbench/connectors`. Proceed by installing your new EMA Workbench configuration, and forcing a reinstallation in case an installation is already in place. Run the following from the root EMAworkbench directory:

```Python setup.py install --force```

After completion, your EMA Workbench installation should now include a Vadere model connector.

## Connection usage
After installation, the Vadere model class can be used just like any other model class within the EMA Workbench. To set up the model initialization, the following arguments are of importance (and required):

- **name**: the name of the modelInterface
- **vadere_jar**: a relative path from the working directory to the Vadere console jar file
- **processor_files**: list of output file names stored by Vadere, depending on set processors. **Note** a .csv file is assumed for timeseries output, and a .txt for a scalar output.
- **model_file**: a relative path from the working directory to the model scenario file
- **wd**: absolute path to working directory. **Note: this path needs to be to an absolute path to a separate directory from the one that holds the Python file initializing the model. Otherwise, the Vadere console version will not work, and parallelization problems arise. All other paths need to be specified relative to this one.**

A demo on how to use the Vadere model connector can be found in the `vadere_connector_demo.ipynb` file, located in this directory. 
