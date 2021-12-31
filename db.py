import sqlite3

create_db = """
CREATE TABLE IF NOT EXISTS REVIEWS
(MOVIE_REVIEW          TEXT    NOT NULL,
PREDICTION             TEXT    NOT NULL,
FEEDBACK               TEXT    NOT NULL);
"""

query_for_all = """
SELECT * FROM REVIEWS
"""

insert_query = """
INSERT INTO REVIEWS VALUES (?, ?, ?);
"""

db_name = "movie_review.db"


def opendb(db_name):
    """
    Function to connect to the DB.
    """
    try:
        conn = sqlite3.connect(db_name)
    except sqlite3.Error:
        return False
    cur = conn.cursor()
    return [conn, cur]


def insert_review(review, prediction, feedback):
    """"
    Function to insert data into DB
    """
    conn, cur = opendb(db_name)
    res = cur.execute(insert_query, (review, prediction, feedback))
    conn.commit()
    conn.close
    return "Inserted Successfully!"    


def create_movie_db():
    """
    Function to create DB
    """
    conn, cur = opendb(db_name)
    cur.execute(create_db)
    conn.close
    return "DB Created Successfully!"


def query_all():
    """
    Function to query all the data from DB
    """
    conn, cur = opendb(db_name)
    res = cur.execute(query_for_all)
    conn.close
    return res


if __name__ == "__main__":
    create_movie_db()
    insert_review(review="sai", prediction="teja", feedback="correct")
    insert_review(review="ram", prediction="sai", feedback="wrong")
    res = query_all()
    for i in res:
        print(i)