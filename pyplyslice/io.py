import typing as t
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import trimesh

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)  # Silence numpy yelling at trimesh


def slice_at_z(mesh: trimesh.Trimesh, slice_z: float) -> trimesh.path.Path3D:
    """Return the slice of the provided mesh, parallel to the XY plane, at the provided Z value."""
    return mesh.section(plane_normal=[0, 0, 1], plane_origin=[0, 0, slice_z])


def slice_to_csv(
    mesh_slice: trimesh.path.Path3D, scan_name: str, slice_z: float, out_dir: Path = Path()
) -> None:
    """
    Dump the vertices of the provided slice to a CSV file.

    Output CSV file name will be built as `<scan_name>_zslice_<slice_z>.CSV`

    Output directory may be optionally specified, but will default to the current working directory.

    NOTE: Coordinate values are output to 3 decimal places.
    NOTE: Contents of any existing output file of the same name will be silently overwritten.
    """
    out_filename = f"{scan_name}_zslice_{slice_z:.0f}.CSV"
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
    NOTE: Entries in the FileName column are assumed to always contain the file extension, which is
    ignored for the comparison.
    """
    scan_data_df = pd.read_excel(filepath, engine="openpyxl", usecols=["FileName", "Z'"])
    scan_data_df.drop_duplicates(subset="FileName", inplace=True)

    return {
        Path(file_name).stem: slice_height
        for file_name, slice_height in scan_data_df.itertuples(index=False)
    }


def slice_pipeline(filepath: Path, slice_z: float, out_dir: t.Optional[Path] = None) -> None:
    """
    Full processing pipeline for slicing the provided PLY file at the specified Z level.

    Output directory may be optionally specified, but will default to the same directory as the
    specified PLY filepath.
    """
    if not out_dir:
        out_dir = filepath.parent

    scan_name = filepath.stem

    mesh = trimesh.load_mesh(filepath)
    mesh_slice = slice_at_z(mesh, slice_z)
    slice_to_csv(mesh_slice, scan_name, slice_z, out_dir)


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

    Where Z' is taken as the height of the slice. All other columns are ignored. The FileName column
    will contain a file extension, which is ignored for the comparison.

    If a PLY file is not present in the spreadsheet then no slice will be taken. Filename comparison
    is case sensitive.

    NOTE: To simplify path case-sensitivity considerations for operating systems that are not
    Windows, scan file extensions are assumed to always be lowercase (`".ply"`).
    """
    slice_heights = parse_slice_heights(key_spreadsheet)

    glob_pattern = "*.ply"
    if recurse:
        glob_pattern = f"**/{glob_pattern}"

    total_count = 0
    found_count = 0
    for scan_filepath in scan_path.glob(glob_pattern):
        total_count += 1
        filename = scan_filepath.stem
        slice_z = slice_heights.get(filename)

        if slice_z:
            found_count += 1
            slice_pipeline(scan_filepath, slice_z, out_dir)
        else:
            print(f"Could not find Z' for '{filename}'")

    print(f"Processing Complete ... Sliced {found_count} of {total_count} PLY files")
