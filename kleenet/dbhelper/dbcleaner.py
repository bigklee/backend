import sqlite3
import re


def extract_year(datstr: str|None):
    if datstr is None:
        return None
    try:
        year = re.findall("[0-9]{4}", datstr)[0]
        return int(year)
    except Exception:
        return None


def replace_kommas(instring):
    return instring.replace(",", ".")


def extract_width(masse: str|None):
    if masse is None:
        return None
    masse = replace_kommas(masse)
    xpos = masse.find("x")
    if xpos == -1:
        return None
    parts = masse.split("x")
    width = re.findall("([0-9]*[.])?[0-9]+", parts[0])[0]
    try:
        return float(width)
    except Exception:
        return None


def extract_height(masse: str|None):
    if masse is None:
        return None
    masse = replace_kommas(masse)
    xpos = masse.find("x")
    if xpos == -1:
        return None
    parts = masse.split("x")
    height = re.findall("([0-9]*[.])?[0-9]+", parts[1])[0]
    try:
        return float(height)
    except Exception:
        return None


if __name__ == "__main__":

    print(extract_height("48,5 x 40,5 cm"))
    print(extract_width("48,5 x 40,5 cm"))

    if True:
        con = sqlite3.connect("/home/dinu/git/bigklee/database/csvimport.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur2 = con.cursor()
        res = cur.execute("DELETE FROM artworks")
        res = cur.execute("SELECT * FROM A_Kunstwerke")
        for i in res:
            cur2.execute(
                "INSERT INTO artworks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    i["ID"],
                    i["TitelDE"],
                    i["TitelEN"],
                    i["Artist"],
                    extract_year(i["Datierung"]),
                    i["WerkNr"],
                    extract_width(i["Masse"]),
                    extract_height(i["Masse"]),
                    i["Mat./Tech.DE"],
                    i["Mat./Tech.EN"],
                    i["Schlagworte"],
                    i["IDverknüpftesWerk"],
                    i["BeschreibungverknüpftesWerk"],
                    i["Institution"]
                )
            )
        con.commit()

