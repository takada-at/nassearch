import csv
import os
import unicodedata

from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin


def normalize(strlike):
    if not isinstance(strlike, str):
        base = str(strlike)
    else:
        base = strlike
    return unicodedata.normalize('NFC', base)


class SearchResult:
    def __init__(self,
                 path: Path,
                 root: Path,
                 display_base: Path,
                 url: str):
        self.path = path
        self.root = root
        self.display_base = display_base
        self.relative = self.path.relative_to(root)
        self.url = url

    def as_data(self) -> List[str]:
        relative = normalize(self.relative)
        return [normalize(self.path.stem),
                normalize(self.display_base / relative),
                os.path.join(self.url, relative)]


class Search:
    def __init__(self,
                 root_dir: str,
                 display_base: str,
                 uri_base: str,
                 ext: str,
                 prefix: Optional[str] = None) -> None:
        self.root_dir = root_dir
        self.uri_base = uri_base
        self.display_base = display_base
        self.ext = ext
        self.path = Path(self.root_dir)
        self.prefix = prefix

    @classmethod
    def safe_read(cls, path: Path) -> bool:
        try:
            return list(path.iterdir())
        except PermissionError as e:
            return []

    def search(self) -> List[SearchResult]:
        stack = []
        if self.prefix:
            for d in self.safe_read(self.path):
                if d.name.startswith(self.prefix):
                    stack.append(d)
        else:
            stack.append(self.path)
        result = []
        while stack:
            target = stack.pop()
            for d in self.safe_read(target):
                if d.is_dir():
                    stack.append(d)
                else:
                    if self.ext is None or d.suffix == self.ext \
                       and not d.name.startswith('.'):
                        result.append(
                            SearchResult(d.resolve(),
                                         Path(self.root_dir),
                                         Path(self.display_base),
                                         self.uri_base))
        return result


def save(savepath: Path, target_setting: Path):
    rules = []
    with target_setting.open() as fp:
        reader = csv.reader(fp)
        for row in reader:
            rules.append(
                Search(row[0], row[1], row[2], row[3], row[4]))
    if savepath.exists():
        savepath.unlink()
    with savepath.open('w') as fp:
        writer = csv.writer(fp)
        for r in rules:
            for r in r.search():
                writer.writerow(r.as_data())
