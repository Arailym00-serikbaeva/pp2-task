import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost"
    )

def init_db():
    """Кестелерді құру: Players және Game Sessions"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
            score INTEGER DEFAULT 0,
            level_reached INTEGER DEFAULT 1,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("База сәтті дайындалды!")

def get_or_create_player(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    conn.commit()
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return player_id

def save_game_session(player_id, score, level):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_top_10():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at 
        FROM game_sessions gs 
        JOIN players p ON gs.player_id = p.id 
        ORDER BY gs.score DESC LIMIT 10
    """)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

def get_personal_best(player_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()  
    return res if res else 0