import pathlib
import sqlite3
from pathlib import Path

from kleenet.models import Artwork, ArtworkCollection


class DatabaseAccessor:

    def __init__(self):
        here = pathlib.Path(__file__).parent.resolve()
        self.connection = sqlite3.connect(str(here / "csvimport.db"))
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_all(self) -> ArtworkCollection:
        objects = []
        res = self.cursor.execute("SELECT * FROM artworks LIMIT 100")
        for i in res:
            objects.append(Artwork.parse_obj(i))
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
