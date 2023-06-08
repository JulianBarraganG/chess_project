import psycopg2
from psycopg2 import sql
from pgntofen import *

#TO BE MODIFIED
YOUR_PASSWORD = 'rotterne'
YOUR_PORT = '3849'

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
        variation VARCHAR,
        string_notation TEXT[]
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
            string_notation = PgnToFen.pgnToStringList('',data[2])
            # SQL statement to insert a row
            insert_row_sql = """
                INSERT INTO Openings (pgn, opening, variation, string_notation)
                VALUES (%s, %s, %s, %s);
            """

            # Execute the SQL statement with the data
            cur.execute(insert_row_sql, (pgn, opening, variation, string_notation))


# Fetch all rows from the result set
select_rows_sql = """
    SELECT *
    FROM Openings;
"""

unique_openings = """
    SELECT DISTINCT opening
    FROM Openings
    ORDER BY opening ASC;
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




#Queries a specific opening by name. Cannot use Variation IS NULL because some openings only exist with their variation name. 
#luckily, it seems that when querieing like this, all of the first results will be the base opening
def specific_opening(opening):
    spec_open = """
    SELECT pgn, string_notation
    FROM Openings
    WHERE opening = %s
    """
    return spec_open, (opening,)

def get_specific_opening(opening):
        query, params = specific_opening(opening)
        cur.execute(query, params)
        result = cur.fetchmany(1)
        return result


def check_for_variations(seq: list):
    # Construct the SQL query with placeholders
    placeholders = ', '.join(['%s'] * len(seq))
    que_vars = f"""
    SELECT pgn
    FROM Openings
    WHERE string_notation[:{len(seq)}] = ARRAY[{placeholders}]
    """
    return que_vars

def get_check_for_variations(seq: list):
    cur.execute(check_for_variations(seq), seq)
    result = cur.fetchall()
    unique_openings_list = [row[0] for row in result]
    return unique_openings_list




unique = get_unique_openings()
# Commit the changes and close the cursor and connection
conn.commit()

"""Lader altså bare være med at lukke de her, fordi ellers kan man ikke tilgå databasen fra app.py. 
Tror det er fint siden vi aldrig skriver noget til databasen"""
#cur.close()
#conn.close()
