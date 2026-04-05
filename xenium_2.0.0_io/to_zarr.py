## Convert the data to zarr format
## Can be run any of the following ways:
##
## python to_zarr.py
## python to_zarr.py -d data -o data.zarr (custom)
## python to_zarr.py --data data --output data.zarr

##
import argparse
import shutil
from pathlib import Path

import spatialdata as sd
from spatialdata_io import xenium

## Constants
ROOT_PROJECT_PATH = Path(__file__).resolve()
DATA_READ_PATH = ROOT_PROJECT_PATH / "data"
DATA_WRITE_PATH = ROOT_PROJECT_PATH / "data.zarr"

## Start

# Use argparse to allow runing script as cli tool
parser = argparse.ArgumentParser(description="Convert data to zarr format")
parser.add_argument(
    "-d",
    "--data",
    type=str,
    default=str(DATA_READ_PATH),
    help="Path to the data to be converted", )
parser.add_argument("-o",
                    "--output",
                    type=str,
                    default=str(DATA_WRITE_PATH),
                    help="Path to where you want to save the data", )
args = parser.parse_args()

# luca's workaround for pycharm
# if not str(path).endswith("xenium_2.0.0_io"):
#     path /= "xenium_2.0.0_io"
#     assert path.exists()

## Parse the data
print(f"parsing the data file: {args.data} ... ", end="")
sdata = xenium(
    path=args.data,
    n_jobs=8,
    cell_boundaries=True,
    nucleus_boundaries=True,
    morphology_focus=True,
    cells_as_circles=True,
#    cleanup_labels_zarr_tmpdir=False,
)
print("Data file successfully parsed")

## Write transformed data to zarr
output_path = Path(args.output)
print(f"writing the data to: {output_path} ... ", end="")
if output_path.exists():
    shutil.rmtree(output_path)
sdata.write(output_path)
print(f"Successfully wrote the data to: {output_path}")

##
sdata = sd.SpatialData.read(f"{output_path}/")
print(sdata)
print(sdata['transcripts']['feature_name'].compute())
##
