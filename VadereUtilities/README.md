# Vadere Utilities
This section holds utilities based on or taken from the original Vadere repository. All original files can be found in the [Vadere repository](https://gitlab.lrz.de/vadere/vadere).

## Spatial data using Open Street Map
We use Open Street Map data to calibrate the pedestrian crowd model on a realistic spatial layout of the Dutch city Breda. This data is publicaly available at the [OSM website](https://www.openstreetmap.org/#map=16/51.5882/4.7770). The data downloaded from OSM can be found [here](https://github.com/floristevito/CrowdSim/blob/main/data/input/files/OSM/Breda_Grote_Markt.osm) and is avaiable under the Open Database Licence, [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright). Therefore, data from OSM and generated files thereoff fall under the [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/) (ODbL).

To convert the spatial layout to Vadere based objects, the osm2vadere converter is used. The used Python script can be found [here](https://github.com/floristevito/CrowdSim/blob/main/VadereUtilities/Converters/osm2vadere/test_osm2vadere.py). 

## Vadere to EMA Workbench connection
