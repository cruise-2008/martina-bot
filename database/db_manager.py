import sqlite3

DB_PATH = 'db.sqlite3'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Убрали ограничение NOT NULL для автоматического заполнения
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            user_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Явно указываем столбцы, чтобы timestamp подставился сам
    cursor.execute(
        'INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)', 
        (user_id, role, content)
    )
    conn.commit()
    conn.close()

def get_history(user_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT role, content FROM messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?', 
            (user_id, limit)
        )
        rows = cursor.fetchall()
        history = [{"role": row[0], "content": row[1]} for row in reversed(rows)]
    except:
        history = []
    conn.close()
    return history

init_db()
