import test_util_dp
from itooth_xiao import util_diagram, util_dp_diagram
from itooth_xiao.util_csv import FileCsvCompound, parse_time


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
