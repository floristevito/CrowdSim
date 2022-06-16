# CrowdSim
This repository acts as a digital appendix in regard to thesis work for a Master of Science in Engineering and Policy Analysis at the Delft University of Technology. It includes:

- `analysis`: All Python utilities used for the analysis.
  - Python scripts for running EMA Workbench based experiments.
  - Python notebook files and scripts for exploring data and generating figures and graphs.
- `data`: All used data files and other resources in the  directory.
  - GIS based images and data files.
  - Input datasets.
  - All generated outcomes using the EMA Workbench.
  - Script used for data conversion.
- `emaConnector`: The EMA Workbench connector to Vadere models.
  - Full source code.
  - Documentation and usage instructions.
- `figures`: An extensive collection of high resolution images and generated graphs.
- `model`: An ABM model made with Vadere of the Grote Markt in Breda, The Netherlands. 
  - The model files included in the `model/model` directory can directly be loaded into the Vadere GUI.
  - All utilized Vadere model scenario files are present, including configurations used for validation purposes.
  - Individual model results are not included due to significant file sizes. These can however be generated by running the model yourself. Note that the seed is set for certain model configurations, such as ones used for validation purposes, to enable reproducibility.
- `vadereUtilities`: Utilities based on tools provided by the Vadere group.
  - The script used for converting OSM data to Vadere objects. 

# Requirements
All Python related instances are tested with Python version 3.10.0. An overview of all requirements can be found in the requirements.txt file in the root of this repository. It is recommended to install them in a Python 3.10.0 environments using:

`pip install -r requirements.txt`

Note that an EMA Workbench installation with the newly added Vadere model connector is needed to run the experimentation scripts included in this repository. See **related works** for more information on how to acquire the right EMA Workbench installation.

# Related work
To reproduce the work of this research in its full extent, related software is needed:

- [Forked and publicly hosted version of Vadere](https://github.com/floristevito/vadere): This Vadere distribution is modified to serve the purposes of this research. To acquire a copy of the source code, make sure to check out the separate branch named "CrowdSim_thesis_floris_additions". Follow the build instructions, as provided on the [Vadere repository](https://gitlab.lrz.de/vadere/vadere), to acquire the needed Vadere console executable.
- [The EMA Workbench](https://github.com/quaquel/EMAworkbench): This research includes the construction of a Vadere/EMA Workbench connector. Although the connector is additionally made available directly within this repository, a complete copy of the workbench including the newly constructed connector can be acquired here. In case the new connector is not yet available on the latest release, please refer to [this forked and publicly hosted version of the EMA workbench](https://github.com/floristevito/EMAworkbench), and check out the branch named "vadere_model_connector". 

## Vadere
This repository is released under the same license as the Vadere library. All orginal, Vadere related software can be found in the [Vadere repository](https://gitlab.lrz.de/vadere/vadere). 
