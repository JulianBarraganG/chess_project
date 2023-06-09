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

# Table for opening database
create_table_sql = """
    DROP TABLE IF EXISTS Openings CASCADE;
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
        next(f)  # Skip the header line1    
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
    ORDER BY opening ASC;
"""

# Queries the pgn for every variation of a given opening
def opening_vars(opening:str) -> list:
    """
    Returns a list of strings, 
    each containing a pgn string matching the opening with all its variations.
    """
    query = """
    SELECT pgn
    FROM Openings
    WHERE opening = %s
    """ 
    cur.execute(query, [opening])
    result = cur.fetchall()
    return [row[0] for row in result]

#takes as input an opening name, and returns a list of lists, each containting a variation
def listOfVars(opening_name: str) -> list:
    """
    Returns a list of list, 
    each sub-list is the base opening or a variation of the opening
    """
    query = opening_vars(opening_name)
    lst = []
    for i in range(len(query)):
        lst.append(PgnToFen.pgnToStringList(query[i]))
    return lst

# Query every unique opening as a list of strings
def get_unique_openings() -> list:
    """
    Returns all the unique openings w/o the variations
    """
    cur.execute(unique_openings)
    result = cur.fetchall()
    unique_openings_list = [row[0] for row in result]
    return unique_openings_list


def get_specific_opening(opening) -> list:
    """
    Returns a list containing the pgn of the unique opening (not a variation)
    """
    lst = listOfVars(opening)
    result = min(lst, key = len)
    return result

unique = get_unique_openings()

# Commit the changes
conn.commit()