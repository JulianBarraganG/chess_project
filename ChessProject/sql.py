import psycopg2
from psycopg2 import sql
from pgntofen import *

#TO BE MODIFIED
YOUR_PASSWORD = 'type your password here'
YOUR_PORT = '4 digit por'

# Establish a connection to server (that you setup yourself). OBS! Check that port, password etc. are correct.
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password= YOUR_PASSWORD,
    port= YOUR_PORT
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

# The 5 file names of the tsv-files
files = ['a','b','c','d','e']

# INSERT HERE -- directory filepath to and with Openings. i.g. below.
your_path = "C:\\Users\\hulig\\OneDrive - University of Copenhagen\\ML\\DIS\\ChessProject\\Openings\\" #remember double backslashes

# Read the TSV file
for file in files:
    with open(your_path+f"{file}.tsv", 'r') as f:
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
    FROM Openings;
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

# Query every unique opening as a list of strings
def get_unique_openings():
    cur.execute(unique_openings)
    result = cur.fetchall()
    unique_openings_list = [row[0] for row in result]
    return unique_openings_list

# Commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()
