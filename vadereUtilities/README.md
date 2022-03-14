# Vadere Utilities
This section holds utilities based on or taken from the original Vadere repository. All original files can be found in the [Vadere repository](https://gitlab.lrz.de/vadere/vadere).

## Spatial data using Open Street Map
We use Open Street Map data to calibrate the pedestrian crowd model on a realistic spatial layout of the Dutch city Breda. This data is publicly available at the [OSM website](https://www.openstreetmap.org/#map=16/51.5882/4.7770). The data downloaded from OSM can be found [here](https://github.com/floristevito/CrowdSim/blob/main/data/input/files/OSM/Breda_Grote_Markt.osm) and is avaiable under the Open Database Licence, [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright). Therefore, data from OSM and generated files thereoff fall under the [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/) (ODbL).

To convert the spatial layout to Vadere based objects, the osm2vadere converter is used. This Python scripts is taken from the orginal Vadere repository, and slightly modefied in order to run it as a standalone script, saving the topography to a .txt file. For the orginal scripts, see the tools in the original [Vadere repository](https://gitlab.lrz.de/vadere/vadere).

### Usage
1. Download the area of interest from [OpenStreetMap](https://www.openstreetmap.org). The file should be in a .osm format.
2. Specify the input and output file name in the Python script.
3. Run the script. 

After these steps, a topography that can be copied into Vadere (open GUI -> select topography -> paste) is present in the specified output .txt file.
