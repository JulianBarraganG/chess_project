import psycopg2
from psycopg2 import sql

# Establish a connection to the database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="rotterne",
    port="3849"
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

# Read the TSV file
with open('C:\\Users\\hulig\\OneDrive - University of Copenhagen\\ML\\DIS\\ChessProject\\Openings\\a.tsv', 'r') as f:
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
    FROM Openings
    LIMIT 10;
"""

cur.execute(select_rows_sql)
rows = cur.fetchall()

# Print the rows
for row in (rows):
    print(row)

# Commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()