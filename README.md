# pyplyslice
Helper Utilities for Slicing PLY Objects at Specific Height(s)

## Installation
This project utilizes [`poetry`](https://python-poetry.org/) for dependency & environment management. Clone or download this repository to your local machine and create a new environment:

```bash
$ cd <project_dir>
$ poetry install
```

Though it's recommended to utilize `poetry`, the project may also be installed via `pip`:

```bash
$ cd <project_dir>
$ pip install .
```

Alternatively, prebuilt binaries for each release are provided at https://github.com/sco1/obj-ply-scaler/releases

## Usage
Once installed, the `pyplyslice` CLI can be invoked directly from the command line:
```bash
$ pyplyslice <inputs go here>
```

Or, if a prebuilt binary is present, this may be called directly
```bash
$ pyplyslice.exe <inputs go here>
```

The `pyplyslice` CLI can also be invoked from the root of this repository using Python:
```bash
$ python ./pyplyslice/ui.py <inputs go here>
```

### `pyplyslice single`
Slice the provided scan file at the specified slice height & output to CSV.

#### Input Parameters
| Parameter         | Description                                     | Type    | Default    |
|-------------------|-------------------------------------------------|---------|------------|
| `--scan-filepath` | Path to PLY file to slice                       | String  | GUI Prompt |
| `--slice-z`       | Z', height above the XY plane to take the slice | Numeric | CLI Prompt |

### `pyplyslice batch`
Batch process all scans in the specified directory using the slice heights spreadsheet key.

#### Input Parameters
| Parameter                  | Description                                                                | Type   | Default    |
|----------------------------|----------------------------------------------------------------------------|--------|------------|
| `--scan-dir`               | Path to directory of PLY files to slice                                    | String | GUI Prompt |
| `--key_spreadsheet`        | Path to excel spreadsheet containing FileName and corresponding Z' columns | String | GUI Prompt |
| `--recurse / --no-recurse` | Recurse through child directories & process all PLY files<sup>1</sup>      | Bool   | `False`    |

**Notes:**
1. When a directory of scans is provided for scaling, to simplify path case-sensitivity considerations for discovery of scan files on operating systems that are not Windows, file extensions are assumed to always be lowercase (e.g. `.ply`).

## Examples
```bash
$ pyplyslice batch --scan-dir "./sample_dir" --key-spreadsheet "./sample_dir/Landmark_XYZ.xlsx"
Processing Complete ... Sliced 82 of 82 PLY files
```

```bash
$ pyplyslice batch --scan-dir "./sample_dir"
# GUI will pop up to select key spreadsheet
Processing Complete ... Sliced 82 of 82 PLY files
```

```bash
$ pyplyslice single --scan-filepath "./sample_dir/some_scan12345-PX-123.edt.123k.ply" --slice-z 25.6
Slicing complete ... sliced 'some_scan12345-PX-123.edt.123k' at Z' = 25.600
```

```bash
$ pyplyslice single --scan-filepath "./sample_dir/some_scan12345-PX-123.edt.123k.ply"
Enter slice height: 25.6
Slicing complete ... sliced 'some_scan12345-PX-123.edt.123k' at Z' = 25.600
```
