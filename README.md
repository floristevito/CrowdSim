# CrowdSim
CrowdSim is the name of this repository holding all the contents in regard to thesis work for a Master of Science in Engineering and Policy Analysis at the Delft University of Technology. It includes:

- An agent-based pedestrian crowd model made with Vadere
- All used data files and other resources
- Generated figures and data-analysis files

# Requirements
All Python related instances are tested with Python version 3.10.0. An overview of all requirements can be found in the requirements.txt file in the root of this repository. It is recommended to install them in an Python 3.10.0 evironments using:

`pip install -r requirements.txt`

# Related work
To reproduce the work of this research in its full extent, related software is needed:

- [Forked and publicly hosted version of Vadere](https://github.com/floristevito/vadere): This Vadere distribution is modified to serve the purposes of this research. To acquire a copy of the source code, make sure to check out the separate branch named "CrowdSim_theis_floris_additions" .
- [The EMA Workbench](https://github.com/quaquel/EMAworkbench): This research includes the construction of a Vadere/EMA Workbench connector. Although the connector is additionally made available directly within this repository, a complete copy of the workbench including the newly constructed connector can be acquired here. In case the new connector is not yet available on the latest release, please refer to [this forked and publicly hosted version of the EMA workbench](https://github.com/floristevito/EMAworkbench), and check out the branch named "vadere_model_connector".

## Vadere
This repository uses software from the Vadere library. This repository is therefore released under the same license as the Vadere library. All orginal, unmodified, Vadere related software can be found in the [Vadere repository](https://gitlab.lrz.de/vadere/vadere). 
