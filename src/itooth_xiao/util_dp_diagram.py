from collections.abc import Callable

from itooth_xiao import util_csv, util_diagram


def read_data(file_csv_compound: util_csv.FileCsvCompound) -> util_diagram.Data:
    file_csv = file_csv_compound.files["dp"]
    vargs: dict[str, list[float | str]] = {}
    for line in file_csv.iter_lines:

        def assign(
            line: util_csv.LineCsv,
            name: str,
            func_convert: Callable[[str], str | float],
        ) -> None:
            text = line.cols[name]
            value = func_convert(text)
            values = vargs.get(name, None)
            if values is None:
                values = []
                vargs[name] = values
            values.append(value)
            # getattr(data, name).append(value)

        for name in util_diagram.NAMES_FLOAT:
            assign(line, name, float)
        for name in util_diagram.NAMES_STR:
            assign(line, name, str)

    return util_diagram.Data(**vargs)  # type: ignore[arg-type]
