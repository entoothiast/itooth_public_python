import test_util_dp
from itooth_xiao import util_diagram, util_dp_diagram
from itooth_xiao.util_csv import FileCsvCompound
import re
import pathlib
from datetime import datetime

RE_FILENAME = re.compile(r"^dp_(?P<datetime>[0-9]{8}-[0-9]{4})_")
"""
https://pythex.org/\n
dp_20250718-1805_0aff_hans-im-glueck
"""


def parse_time(filename: pathlib.Path) -> float:
    match_filename = RE_FILENAME.match(filename.stem)
    if match_filename is None:
        return 0.0
        # raise ValueError(f"Could not parse date/time: {filename}")
    _datetime = match_filename.group("datetime")
    dt = datetime.strptime(_datetime, "%Y%m%d-%H%M")
    return dt.timestamp()


def test_diagram():
    dp_filename = (
        test_util_dp.DIRECTORY_SAMPLES / "dp_yyyymmdd-hhmm_0a48_add-comment0405.csv"
    )
    for dp_filename in test_util_dp.iter_sample_files():
        file_csv_compound = FileCsvCompound.factory(dp_filename)
        time_s = parse_time(dp_filename)
        data = util_dp_diagram.read_data(file_csv_compound=file_csv_compound)
        util_diagram.diagram(
            data=data,
            time_s=time_s,
            show=False,
            filename=dp_filename.with_suffix(".png"),
        )


if __name__ == "__main__":
    test_diagram()
