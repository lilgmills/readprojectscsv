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

def main():
    example()
    return

if __name__ == "__main__":
    main()
