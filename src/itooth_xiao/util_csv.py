from __future__ import annotations

import dataclasses
import pathlib
import re
from collections.abc import Iterator
from datetime import datetime

RE_FILENAME = re.compile(r"^dp_(?P<datetime>[0-9]{8}-[0-9]{4})_")
"""
https://pythex.org/\n
dp_20250718-1805_0aff_hans-im-glueck
"""


def parse_time(filename: pathlib.Path) -> float:
    assert isinstance(filename, pathlib.Path)

    match_filename = RE_FILENAME.match(filename.stem)
    if match_filename is None:
        return 0.0
        # raise ValueError(f"Could not parse date/time: {filename}")
    _datetime = match_filename.group("datetime")
    dt = datetime.strptime(_datetime, "%Y%m%d-%H%M")
    return dt.timestamp()


@dataclasses.dataclass(slots=True, frozen=True)
class LineCsv:
    file_csv: FileCsv
    cols: dict[str, str]

    def dump(self, f) -> None:
        print(f"  {self.cols!r}", file=f)


@dataclasses.dataclass(slots=True, frozen=True)
class FileCsv:
    tag: str
    header: str
    lines: list[str] = dataclasses.field(default_factory=list)

    @property
    def iter_lines(self) -> Iterator[LineCsv]:
        cols_header = self.header.split(",")
        for line in self.lines:
            cols_line = line.split(",")
            cols: dict[str, str] = {}
            for col_header, col_line in zip(cols_header, cols_line, strict=False):
                cols[col_header] = col_line
            yield LineCsv(file_csv=self, cols=cols)

    def dump(self, f) -> None:
        print(f"######### {self.tag}", file=f)
        for line in self.iter_lines:
            line.dump(f)


@dataclasses.dataclass(slots=True, frozen=True)
class FileCsvCompound:
    files: dict[str, FileCsv]

    def dump(self, f) -> None:
        for file_csv in self.files.values():
            file_csv.dump(f)

    @staticmethod
    def factory(filename: pathlib.Path) -> FileCsvCompound:
        files: dict[str, FileCsv] = {}
        for line in filename.read_text().splitlines():
            cols = line.split(",", 1)
            tag = cols[0]
            file_csv = files.get(tag, None)
            if file_csv is None:
                file_csv = FileCsv(tag=tag, header=line)
                files[tag] = file_csv
                continue

            file_csv.lines.append(line)

        return FileCsvCompound(files=files)
        # return FileCsvCompound(files=sorted(files.values(), key=lambda f: f.tag))
