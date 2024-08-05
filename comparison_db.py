import sqlite3

def example():
    data = {
        1: {2, 3},
        2: {3},
        3: set()
    }

    conn = sqlite3.connect('comparisons.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comparisons (
        key INTEGER PRIMARY KEY,
        better_than TEXT
    )
    ''')

    for key, better_than in data.items():
        cursor.execute('INSERT OR REPLACE INTO comparisons (key, better_than) VALUES (?, ?)',
                    (key, ','.join(map(str, better_than))))

    conn.commit()
    conn.close()
    return

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create the comparisons table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS comparisons (
                       key INTEGER PRIMARY KEY,
                       better_than TEXT
                       )
                       ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_comparison(conn, key, better_than):
    """Insert a new comparison into the comparisons table."""
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO comparisons (key, better_than) VALUES (?, ?)', (key, better_than))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def update_comparisons_from_file(conn, filename):
    """Update the comparisons table with records from the file."""
    with open(filename, 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            insert_comparison(conn, index, line.strip())

def main():
    example()
    return

if __name__ == "__main__":
    main()
