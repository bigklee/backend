import pathlib
import sqlite3
from pathlib import Path

from kleenet.models import Artwork, ArtworkCollection, Filters, Collection, CollectionList


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

    @staticmethod
    def _keyword_present(needle, haystack) -> bool:
        if haystack is None:
            return False
        return needle in haystack

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
            needles = keyword.split(",")
            for j in needles:
                objects = list(filter(lambda x: self._keyword_present(j, x.keywords), objects))
        if linked_work is not None:
            objects = list(filter(lambda x: linked_work in x.linked_works, objects))
        return ArtworkCollection(__root__=objects)

    def get_by_id(self, id_: int) -> Artwork | None:
        res = self.cursor.execute("SELECT * FROM artworks WHERE id=?", (id_,))
        obj = res.fetchone()
        if obj is None:
            return None
        return Artwork.parse_obj(obj)

    def get_filters(self) -> Filters:
        res = self.cursor.execute("SELECT * FROM keywords")
        keywords = [i["keyword"] for i in res]
        res = self.cursor.execute("SELECT year FROM artworks GROUP BY year")
        years = [i["year"] for i in res if i["year"] is not None]
        return Filters(keywords=keywords, years=years)

    def get_collections(self, collection_id: int | None = None):
        if collection_id is None:
            res = self.cursor.execute('''SELECT id, name, author FROM collections''')
            collections = []
            for i in res:
                collections.append(Collection(collection_id=i["id"], name=i["name"], author=i["author"]))
            return CollectionList(__root__=collections)
        else:
            res1 = self.cursor.execute("SELECT id, name, author FROM collections WHERE id=?", (collection_id,))
            obj = res1.fetchone()
            if obj is None:
                return None
            col_id = obj["id"]
            col_name = obj["name"]
            col_author = obj["author"]
            res = self.cursor.execute('''
                SELECT * FROM collections 
                JOIN incollection ON collections.id=incollection.collection_id
                JOIN artworks ON artworks.id=incollection.artwork_id
                WHERE collections.id=?
            ''', (collection_id,))
            works = []
            for i in res:
                works.append(Artwork.parse_obj(i))
            return Collection(
                collection_id=col_id,
                name=col_name,
                author=col_author,
                works=ArtworkCollection(__root__=works)
            )

    def to_file(self, c: ArtworkCollection):
        p = Path("/tmp/exporttest.json")
        with p.open('w') as f:
            f.write(c.json())


if __name__ == "__main__":
    db = DatabaseAccessor()
    res = db.get_collections(2)
    print(res)

