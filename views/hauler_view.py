import sqlite3
import json

def update_hauler(id, hauler_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Hauler
                SET
                    name = ?,
                    dock_id = ?
            WHERE id = ?
            """,
            (hauler_data['name'], hauler_data['dock_id'], id)
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_hauler(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Hauler WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_haulers(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if "_embed" in url["query_params"]:
            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                h.id haulerId,
                h.name haulerName,
                h.dock_id,
                s.id id,
                s.name name,
                s.hauler_id
            FROM Hauler h
            LEFT JOIN Ship s
                ON h.id = s.hauler_id
            """)
            query_results = db_cursor.fetchall()

            haulers = {} #! initializes the empty dictionary
            for row in query_results:
                hauler_id = row["haulerId"]
                #! this logic checks to see if the hauler is in the haulers dict
                #! if hauler is not in the dict, then it adds it and the ship associated to the hauler dict
                #! if it is in the dictionary, just adds the associated ship to the hauler
                if hauler_id not in haulers:
                    haulers[hauler_id] = {
                        "id": row['haulerId'],
                        "name": row['haulerName'],
                        "dock_id": row["dock_id"],
                        "ships": []
                    }
                ship = {
                "id": row['id'],
                "name": row['name'],
                "hauler_id": row["hauler_id"],
            }
                haulers[hauler_id]["ships"].append(ship) #! adds ship to the ships list

            serialized_haulers = json.dumps(list(haulers.values()))
            
              
        else:
            # # Write the SQL query to get the information you want
            # db_cursor.execute("""
            # SELECT
            #     s.id,
            #     s.name,
            #     s.hauler_id
            # FROM Ship s
            # """)
            # query_results = db_cursor.fetchall()

        # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                h.id,
                h.name,
                h.dock_id
            FROM Hauler h
            """)
            query_results = db_cursor.fetchall()

            # Initialize an empty list and then add each dictionary to it
            haulers=[]
            for row in query_results:
                haulers.append(dict(row))

        # Serialize Python list to JSON encoded string
            serialized_haulers = json.dumps(haulers)

    return serialized_haulers

def retrieve_hauler(pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            h.id,
            h.name,
            h.dock_id
        FROM Hauler h
        WHERE h.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        serialized_hauler = json.dumps(dict(query_results))

    return serialized_hauler
