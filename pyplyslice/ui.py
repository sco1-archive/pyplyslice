import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import typer
from pyplyslice import io


pyplyslice_cli = typer.Typer()


@pyplyslice_cli.command()
def single(
    scan_filepath: Path = typer.Option(None, exists=True, file_okay=True, dir_okay=False),
    slice_z: float = typer.Option(None, prompt="Enter slice height"),
) -> None:
    """Slice the provided scan file at the specified slice height & output to CSV."""
    if scan_filepath is None:
        scan_filepath = _prompt_for_file()

    io.slice_pipeline(scan_filepath, slice_z)


@pyplyslice_cli.command()
def batch(
    scan_dir: Path = typer.Option(None, exists=True, file_okay=False, dir_okay=True),
    key_spreadsheet: Path = typer.Option(None, exists=True, file_okay=True, dir_okay=False),
    recurse: bool = False,
) -> None:
    """
    Batch process all scans in the specified directory using the slice heights spreadsheet key.

    Recursive processing may be optionally specified (Default: False).
    """
    if scan_dir is None:
        scan_dir = _prompt_for_dir()

    if key_spreadsheet is None:
        key_spreadsheet = _prompt_for_file()

    io.batch_slice_pipeline(scan_dir, key_spreadsheet, recurse=recurse)


@pyplyslice_cli.callback(invoke_without_command=True, no_args_is_help=True)
def main(ctx: typer.Context) -> None:  # pragma: no cover
    """Helper utilities for slicing PLY objects at specific heights."""
    # Provide a callback for the base invocation to display the help text & exit.
    pass


def _prompt_for_file(start_dir: Path = Path()) -> Path:  # pragma: no cover
    """Open a Tk file selection dialog to prompt the user to select a single file for processing."""
    root = tk.Tk()
    root.withdraw()

    return Path(
        filedialog.askopenfilename(
            title="Select scan file for processing.", initialdir=start_dir, multiple=False,
        )
    )


def _prompt_for_dir(start_dir: Path = Path()) -> Path:  # pragma: no cover
    """Open a Tk file selection dialog to prompt the user to select a directory for processing."""
    root = tk.Tk()
    root.withdraw()

    return Path(
        filedialog.askdirectory(
            title="Select scan directory for batch processing.", initialdir=start_dir,
        )
    )


if __name__ == "__main__":  # pragma: no cover
    pyplyslice_cli()
