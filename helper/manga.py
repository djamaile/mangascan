from dataclasses import dataclass


@dataclass(frozen=True)
class Manga:
    __slots__ = ["name", "img", "link", "publisher"]
    name: str
    img: str
    link: str
    publisher: str
