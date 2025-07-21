"""
Where to take the tests from
--micropython-tests-giturl=https://github.com/dpgeorge/micropython.git@tests-full-test-runner

Where to take the firmware from
--firmware-build-giturl=https://github.com/micropython/micropython.git@v1.24.1
--firmware-build-gitdir=~/micropython
--firmware-gitdir=~/micropython
"""

from __future__ import annotations

import logging
import pathlib

import typer
import typing_extensions

from itooth_xiao import util_csv, util_diagram, util_dp_diagram

logger = logging.getLogger(__file__)

# 'typer' does not work correctly with typing.Annotated
# Required is: typing_extensions.Annotated
TyperAnnotated = typing_extensions.Annotated

# mypy: disable-error-code="valid-type"
# This will disable this warning:
#   op.py:58: error: Variable "octoprobe.scripts.op.TyperAnnotated" is not valid as a type  [valid-type]
#   op.py:58: note: See https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases

app = typer.Typer(pretty_exceptions_enable=False)

MATCH_FILES = "**/dp_*.csv"


@app.command(help="Find csv files and create png diagrams")
def render(
    directory: TyperAnnotated[
        str,
        typer.Option(
            help="Directory to search csv files. This may point to a csv file too.",
        ),
    ] = ".",
    match: TyperAnnotated[
        str | None,
        typer.Option(help="The pattern to search files."),
    ] = MATCH_FILES,  # noqa: UP007
    dpi: TyperAnnotated[
        int | None,
        typer.Option(help="The resolution of the image"),
    ] = 600,  # noqa: UP007
    remove: TyperAnnotated[
        bool | None,
        typer.Option(help="Remove the png files."),
    ] = False,  # noqa: UP007
    show: TyperAnnotated[
        bool | None,
        typer.Option(help="Show the diagram and do not create a png."),
    ] = False,  # noqa: UP007
) -> None:
    _directory = pathlib.Path(directory).expanduser()
    if _directory.is_file():
        directories = [_directory]
    elif _directory.is_dir():
        directories = list(_directory.glob(match))
    else:
        print(f"ERROR: does not exist: {_directory}")
        raise typer.Exit(-5)

    if len(directories) == 0:
        print(
            f"INFO: No files matching '{match}' found in this directory: {_directory}"
        )

    for csv_filename in directories:
        png_filename = csv_filename.with_suffix(".png")
        if remove:
            print(f"Remove: {png_filename}")
            png_filename.unlink(missing_ok=True)
            continue
        try:
            print(f"Diagram: {png_filename}")
            file_csv_compound = util_csv.FileCsvCompound.factory(csv_filename)
            data = util_dp_diagram.read_data(file_csv_compound=file_csv_compound)
            time_s = util_csv.parse_time(csv_filename)
            util_diagram.diagram(
                data=data,
                time_s=time_s,
                show=show,
                filename=None if show else png_filename,
                dpi=dpi,
            )
        except Exception as e:
            print(f"ERROR: {csv_filename}\n{e!r}")

    raise typer.Exit(0)


if __name__ == "__main__":
    app()
