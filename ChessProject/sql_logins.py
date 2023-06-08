import psycopg2
from psycopg2 import sql

# Database connection configuration
#TO BE MODIFIED
YOUR_PASSWORD = 'vxz73ptw'
YOUR_PORT = '5432'

# Establish a connection to server (that you setup yourself). OBS! Check that port, password etc. are correct.
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password= YOUR_PASSWORD,
    port= YOUR_PORT
)

cur = conn.cursor()

create_log_table = """
    DROP TABLE IF EXISTS Users;
    CREATE TABLE Users (
        id SERIAL PRIMARY KEY,
        username VARCHAR UNIQUE,
        password VARCHAR
    );
    """
    
cur.execute(create_log_table)
    
conn.commit()