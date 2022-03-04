# Vadere EMA Workbench connector
This section holds the in this research build model connector from the [EMA Workbench](https://github.com/quaquel/EMAworkbench) to Vadere. The connector is intended to be included in the EMA Workbench source-code in the future. An instruction on the use of the model connector can be found below.

## Connector configuration
As long as the connector is not yet included in the newest EMA Workbench distribution, the configuration below has to be performed by the user manually. This will become absolute in the near future.

First, get a copy of this repository and locate the `vadere.py` file included in this section. This file serves as the model connector. Secondly, get a copy of the EMA Workbench source code and make sure your Python environment is up-to-date with all the EMA Workbench requirements. 

After all the files are obtained, place the `vadere.py` file inside your EMA Workbench copy under `ema_workbench/connectors`. Proceed by installing your new EMA Workbench configuration, and forcing a reinstallation in case an installation is already in place. Run the following from the root EMAworkbench directory:

```Python setup.py install --force```

After completion, your EMA Workbench installation should now include a Vadere model connector.

## Model connection usage
