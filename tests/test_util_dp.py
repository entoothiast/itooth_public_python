import pathlib
import sys
from collections.abc import Iterator

from itooth_xiao.util_csv import FileCsvCompound

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent
DIRECTORY_PYTHON = DIRECTORY_OF_THIS_FILE.parent
DIRECTORY_NAME_SAMPLES = "sample_dp_files"
DIRECTORY_SAMPLES = DIRECTORY_PYTHON / DIRECTORY_NAME_SAMPLES
assert DIRECTORY_SAMPLES.is_dir()


def iter_sample_files() -> Iterator[pathlib.Path]:
    return DIRECTORY_SAMPLES.glob("**/dp_*.csv")


def test_dp():
    for dp_filename in iter_sample_files():
        print(dp_filename.name)
        file_csv_compound = FileCsvCompound.factory(dp_filename)
        file_csv_compound.dump(f=sys.stdout)


if __name__ == "__main__":
    test_dp()
