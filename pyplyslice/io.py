import typing as t
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import trimesh

warnings.filterwarnings(
    "ignore", category=np.VisibleDeprecationWarning
)  # Silence numpy yelling at trimesh


def calculate_plane_normal(landmarks: pd.DataFrame) -> np.ndarray:
    """
    Calculate the normal vector for the desired slicing plane.

    The slicing plane is defined by the triangle formed by the following landmarks:
        * Tragion Left   ("f_t_l")
        * Tragion Right  ("r_t_r")
        * Orbitale Right ("k_or_r")
    """
    tri = landmarks[["r_t_r", "f_t_l", "k_or_r"]]
    normals, _ = trimesh.triangles.normals(triangles=tri)  # Ignore the "is face nonzero" bool

    return normals.squeeze()  # We only gave one triangle we can squeeze this down to the one normal


def slice_at_glabella(
    mesh: trimesh.Trimesh, landmarks: pd.DataFrame, z_offset_mm: float = 15
) -> trimesh.path.Path3D:
    """
    Slice the provided mesh parallel to the calculated slicing plane at the provided z offset.

    Slicing plane is determined by the `calculate_plane_normal` command using a predefined set of
    landmarks. See the function's documentation for more information.

    Slice plane origin uses the glabella XY coordinates, along with the Z coordinate offset by
    `z_offset_mm`, which defaults to 15 mm.
    """
    plane_normal = calculate_plane_normal(landmarks)
    plane_origin_xyz = landmarks["h_g"]  # Use glabella as slicing plane origin
    plane_origin_xyz.z += z_offset_mm

    return mesh.section(plane_normal=plane_normal, plane_origin=plane_origin_xyz)


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
    np.savetxt(
        out_filepath, mesh_slice.vertices, fmt="%.3f", delimiter=",", comments="", header="x,y,z"
    )


def parse_landmarks(filepath: Path) -> pd.DataFrame:
    """
    Parse the provided landmark *.txt file into a DataFrame.

    Landmark *.txt files are assumed to be space delimited (name x y z) rows with 1 header line.

    The resulting DataFrame will be transposed so the landmark names serve as column headers & XYZ
    coordinates lie along the rows. This is to provide the correct format for trimesh's normal
    vector calculations.
    """
    return pd.read_csv(filepath, sep=" ", index_col=0).T


def slice_pipeline(filepath: Path, slice_z: float, out_dir: t.Optional[Path] = None) -> None:
    """
    Full processing pipeline for slicing the provided PLY file at the specified Z level.

    Output directory may be optionally specified, but will default to the same directory as the
    specified PLY filepath.
    """
    raise NotImplementedError
    if not out_dir:
        out_dir = filepath.parent

    scan_name = filepath.stem

    mesh = trimesh.load_mesh(filepath)
    mesh_slice = slice_at_z(mesh, slice_z)
    slice_to_csv(mesh_slice, scan_name, slice_z, out_dir)

    print(f"Slicing complete ... sliced '{scan_name}' at Z' = {slice_z:.3f}")


def batch_slice_pipeline(
    scan_path: Path, out_dir: t.Optional[Path] = None, recurse: t.Optional[bool] = False,
) -> None:
    """
    Slice all PLY files in the provided path using data from its corresponding landmark file.

    Recursion may be optionally specified with the `recurse` kwarg, which defaults to `False`.

    NOTE: To simplify path case-sensitivity considerations for operating systems that are not
    Windows, scan file extensions are assumed to always be lowercase (`".ply"`).
    """
    raise NotImplementedError

    glob_pattern = "*.ply"
    if recurse:
        glob_pattern = f"**/{glob_pattern}"

    total_count = 0
    found_count = 0
    for scan_filepath in scan_path.glob(glob_pattern):
        total_count += 1
        filename = scan_filepath.stem
        slice_z = slice_heights.get(filename)  # TODO: Refactor to parse from landmark .txt

        if slice_z:
            found_count += 1
            slice_pipeline(scan_filepath, slice_z, out_dir)
        else:
            print(f"Could not find Z' for '{filename}'")

    print(f"Processing Complete ... Sliced {found_count} of {total_count} PLY files")
