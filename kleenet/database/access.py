import pathlib
import sqlite3
from pathlib import Path

from kleenet.models import Artwork, ArtworkCollection


class DatabaseAccessor:

    SIZE_EPSILON = 5

    def __init__(self):
        here = pathlib.Path(__file__).parent.resolve()
        self.connection = sqlite3.connect(str(here / "csvimport.db"))
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    @staticmethod
    def _assemble_query(
            title_de: str | None = None,    # in sql
            title_en: str | None = None,    # in sql
            artist: str | None = None,      # in sql
            year: int | None = None,        # in sql
            work_no: str | None = None,     # in sql
            width: float | None = None,     # in python
            height: float | None = None,    # in python
            keyword: str | None = None,     # in python
            linked_work: int | None = None, # in python
            institution: str | None = None  # in sql
    ) -> (str, tuple):
        params = ()
        query = "SELECT * FROM artworks WHERE 1=1 "
        if title_de is not None:
            query += "AND title_de == ? "
            params += (title_de,)
        if title_en is not None:
            query += "AND title_en == ? "
            params += (title_en,)
        if artist is not None:
            query += "AND artist == ? "
            params += (artist,)
        if year is not None:
            query += "AND year == ? "
            params += (year,)
        if work_no is not None:
            query += "AND work_no == ? "
            params += (work_no,)
        if institution is not None:
            query += "AND institution == ? "
            params += (institution,)
        query += "LIMIT 100"
        pass
        return query, params

    @staticmethod
    def _check_size_contraint(size: float | None, target_size: float) -> bool:
        if size is None:
            return False
        if target_size - DatabaseAccessor.SIZE_EPSILON < size < target_size + DatabaseAccessor.SIZE_EPSILON:
            return True
        return False

    def get_all(
            self,
            title_de: str | None = None,      # in sql
            title_en: str | None = None,      # in sql
            artist: str | None = None,        # in sql
            year: int | None = None,          # in sql
            work_no: str | None = None,       # in sql
            width: float | None = None,       # in python
            height: float | None = None,      # in python
            keyword: str | None = None,       # in python
            linked_work: int | None = None,   # in python
            institution: str | None = None    # in sql
    ) -> ArtworkCollection:
        objects = []
        query = self._assemble_query(
            title_de,
            title_en,
            artist,
            year,
            work_no,
            width,
            height,
            keyword,
            linked_work,
            institution
        )
        res = self.cursor.execute(query[0], query[1])
        for i in res:
            objects.append(Artwork.parse_obj(i))
        if height is not None:
            objects = list(filter(lambda x: self._check_size_contraint(x.height, height), objects))
        if width is not None:
            objects = list(filter(lambda x: self._check_size_contraint(x.width, width), objects))
        if keyword is not None:
            objects = list(filter(lambda x: keyword in x.keywords, objects))
        if linked_work is not None:
            objects = list(filter(lambda x: linked_work in x.linked_works, objects))
        pass
        return ArtworkCollection(__root__=objects)

    def get_by_id(self, id_: int) -> Artwork | None:
        res = self.cursor.execute("SELECT * FROM artworks WHERE id=?", (id_,))
        obj = res.fetchone()
        if obj is None:
            return None
        return Artwork.parse_obj(obj)

    def to_file(self, c: ArtworkCollection):
        p = Path("/tmp/exporttest.json")
        with p.open('w') as f:
            f.write(c.json())


if __name__ == "__main__":
    db = DatabaseAccessor()
    o = db.get_all()
    db.to_file(o)
