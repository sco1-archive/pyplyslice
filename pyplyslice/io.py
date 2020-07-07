import typing as t
from pathlib import Path

import numpy as np
import pandas as pd
import trimesh


def slice_at_z(mesh: trimesh.Trimesh, z: float) -> trimesh.path.Path3D:
    """Return the slice of the provided mesh, parallel to the XY plane, at the provided Z value."""
    return mesh.section(plane_normal=[0, 0, 1], plane_origin=[0, 0, z])


def slice_to_csv(
    mesh_slice: trimesh.path.Path3D, scan_name: str, z: float, out_dir: Path = Path()
) -> None:
    """
    Dump the vertices of the provided slice to a CSV file.

    Output CSV file name will be built as `<scan_name>_zslice_<z>.CSV`

    Output directory may be optionally specified, but will default to the current working directory.

    NOTE: Coordinate values are output to 3 decimal places.
    NOTE: Contents of any existing output file of the same name will be silently overwritten.
    """
    out_filename = f"{scan_name}_zslice_{z}.CSV"
    out_filepath = out_dir / out_filename

    # `mesh_slice.vertices` is just a numpy array in disguise, so we can dump it directly
    np.savetxt(out_filepath, mesh_slice.vertices, fmt="%.3f", delimiter=",", header="x,y,z")


def parse_slice_heights(filepath: Path) -> t.Dict[str, float]:
    """
    Parse the provided *.xlsx file into a dictionary containing file name, slice height KV pairs.

    The input *.xlsx file must contain at least the following columns:
        * FileName
        * Z'

    Where Z' is taken as the height of the slice. All other columns are ignored.

    NOTE: Any duplicate FileName entries are dropped, the first seen value will be retained as the
    slice height for the file. File names are case sensitive.
    NOTE: FileName will be the name of the scan file without the *.PLY extension
    """
    scan_data_df = pd.read_excel(filepath, engine="openpyxl", usecols=["FileName", "Z'"])
    scan_data_df.drop_duplicates(subset="FileName", inplace=True)

    return {
        file_name: slice_height for file_name, slice_height in scan_data_df.itertuples(index=False)
    }


def slice_pipeline(filepath: Path, z: float, out_dir: t.Optional[Path] = None) -> None:
    """
    Full processing pipeline for slicing the provided PLY file at the specified Z level.

    Output directory may be optionally specified, but will default to the same directory as the
    specified PLY filepath.
    """
    if not out_dir:
        out_dir = filepath.parent

    scan_name = filepath.stem

    mesh = trimesh.load_mesh(filepath)
    mesh_slice = slice_at_z(mesh, z)
    slice_to_csv(mesh_slice, scan_name, z, out_dir)


def batch_slice_pipeline(
    scan_path: Path,
    key_spreadsheet: Path,
    out_dir: t.Optional[Path] = None,
    recurse: t.Optional[bool] = False,
) -> None:
    """
    Slice all PLY files in the provided path using data from the corresponding spreadsheet.

    Recursion may be optionally specified with the `recurse` kwarg, which defaults to `False`.

    `key_spreadsheet` is an Excel file that must contain at least the following columns:
        * FileName
        * Z'

    Where Z' is taken as the height of the slice. All other columns are ignored.

    If a PLY file is not present in the spreadsheet then no slice will be taken. Filename comparison
    is case sensitive.

    NOTE: To simplify path case-sensitivity considerations for operating systems that are not
    Windows, scan file extensions are assumed to always be lowercase (`".ply"`).
    """
    raise NotImplementedError
