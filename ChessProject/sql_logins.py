import sql

cur = sql.conn.cursor()

create_users_table = """
    DROP TABLE IF EXISTS Users CASCADE;
    CREATE TABLE Users (
        id SERIAL PRIMARY KEY,
        username VARCHAR UNIQUE,
        password VARCHAR
    );
    """
def create_users_table():
    """
    This function creates the users table, if it doesn't already exist in the database.
    This ensures that the database keeps all the users in the table.
    """
    # Establish connection
    cur = sql.conn.cursor()

    # Check if the table exists
    cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = 'users');")
    table_exists = cur.fetchone()[0]
    print(table_exists)

    if not table_exists:
        print("Creating table from scratch")
        # Create the table if it doesn't exist
        cur.execute(create_users_table)
        sql.conn.commit()
    else:
        print("We already have this table")
    cur.close()


# er vel en many-to-many... en user kan have mange favorite openings, 
# og openings kan være favorite af mange users.
# bruger pgn som key, og lave hjælpe-insertfunktion til at tilføje navn
create_fav_open_relation = """
    DROP TABLE IF EXISTS Fav_Open;
    CREATE TABLE Fav_Open (
        userID INT PRIMARY KEY,
        opening_pgn VARCHAR,
        opening_name VARCHAR,
        
        CONSTRAINT fk_openings FOREIGN KEY (opening_pgn) REFERENCES Openings(pgn),
        CONSTRAINT fk_userID FOREIGN KEY (userID) REFERENCES Users(id)
    );
    """

#intentionen er at lave en funktion der vil indsætte fav opening,
# med alle kolloner udfyldt.
def InsertOpenFavOpen(user:int,pgn:str):
    #get name for the insert
    get_name_query = f"""
    SELECT DISTINCT opening
    FROM Openings
    WHERE pgn = '{pgn}'
    """
    
    cur.execute(get_name_query)
    name = cur.fetchone()[0]
    
    # sql query:
    insert_query = f"""
    INSERT INTO Fav_Open (userID, opening_pgn, opening_name) VALUES ({user}, '{pgn}', '{name}')
    """
    
    return insert_query


#cur.execute(create_fav_open_relation)
sql.conn.commit()