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

## Usage
Once installed, the `pyplyslice` CLI can be invoked directly from the command line:
```bash
$ pyplyslice <inputs go here>
```

The `pyplyslice` CLI can also be invoked from the root of this repository using Python:
```bash
$ python ./pyplyslice/ui.py <inputs go here>
```

For all processing pipelines, slice heights are calculated from the PLY file's associated `*.txt` file containing the scan's landmark coordinates. The landmarks file is assumed to have the same stem as the PLY file. Association of landmarks file to PLY file is case sensitive. If a landmarks file cannot be found, the PLY is skipped.

Landmark `*.txt` files are assumed to be space delimited rows (`name x y z`) with 1 header line.

Helper Jupyter Notebooks are also provided in the root of the repository to handle basic tasks.

### `pyplyslice single`
Slice the provided scan file and output to CSV.

#### Input Parameters
| Parameter         | Description                                     | Type    | Default    |
|-------------------|-------------------------------------------------|---------|------------|
| `--scan-filepath` | Path to PLY file to slice                       | String  | GUI Prompt |

### `pyplyslice batch`
Batch process all scans in the specified directory and output to CSVs.

#### Input Parameters
| Parameter                  | Description                                                                | Type   | Default    |
|----------------------------|----------------------------------------------------------------------------|--------|------------|
| `--scan-dir`               | Path to directory of PLY files to slice                                    | String | GUI Prompt |
| `--recurse / --no-recurse` | Recurse through child directories & process all PLY files<sup>1</sup>      | Bool   | `False`    |

**Notes:**
1. When a directory of scans is provided for scaling, to simplify path case-sensitivity considerations for discovery of scan files on operating systems that are not Windows, file extensions are assumed to always be lowercase (e.g. `.ply`).

## Examples
```bash
$ pyplyslice batch --scan-dir "./sample_dir"
# <snip>
Processing Complete ... Sliced 82 of 82 PLY files
```

```bash
$ pyplyslice single --scan-filepath "./sample_dir/some_scan12345-PX-123.edt.123k.ply" --slice-z 25.6
Slicing complete ... sliced 'some_scan12345-PX-123.edt.123k' at Z' = 25.600
```
