import psycopg2
from psycopg2 import sql
from pgntofen import *


# Establish a connection to the database. Make sure to change stringnames to your server.
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="vxz73ptw",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

create_table_sql = """
    DROP TABLE IF EXISTS Openings;
    CREATE TABLE Openings (
        pgn VARCHAR PRIMARY KEY,
        opening VARCHAR,
        variation VARCHAR
    );
"""

cur.execute(create_table_sql)

files = ['a','b','c','d','e']

# Read the TSV file
for file in files:
    with open(f'C:\\Users\\Kaest\\Documents\\KU\\2_Semester\\DIS\\Projekt\\chess_project\\ChessProject\\Openings\\{file}.tsv', 'r') as f:
        next(f)  # Skip the header line
        for line in f:
            data = line.strip().split('\t')
            pgn = data[2]
            opening = data[1].split(':')[0] if ':' in data[1] else data[1]
            variation = data[1].split(':')[1] if ':' in data[1] else None

            # SQL statement to insert a row
            insert_row_sql = """
                INSERT INTO Openings (pgn, opening, variation)
                VALUES (%s, %s, %s);
            """

            # Execute the SQL statement with the data
            cur.execute(insert_row_sql, (pgn, opening, variation))


# Fetch all rows from the result set

select_rows_sql = """
    SELECT *
    FROM Openings;
"""

unique_openings = """
    SELECT DISTINCT opening
    FROM Openings
    WHERE variation IS NULL;
"""

# Queries the pgn for every variation of a given opening
def opening_vars(open:str):
    que_vars = f"""
    SELECT pgn
    FROM Openings
    WHERE opening = '{open}'
    """
    return (que_vars)

#takes as input an opening name, and returns a list of lists, each containting a variation
def listOfVars(opening_name: str) -> list:
    cur.execute(opening_vars(opening_name))
    query = cur.fetchall()
    lst = []
    for i in range(len(query)):
        lst.append(PgnToFen.pgnToStringList(query[i][0]))
    return lst

def get_unique():
    cur.execute(unique_openings)
    return (cur.fetchall())


print(get_unique())

# Commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()
