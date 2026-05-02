import psycopg2  # PostgreSQL деректер қорымен байланысу үшін қажетті кітапхана

# Деректер қорына қосылу функциясы
def get_db_connection():
    return psycopg2.connect(
        dbname="snake_game",  
        user="postgres",      
        password="1234",      
        host="localhost",    
        port="5432"           
    )

# Ойыншыны табу немесе жаңадан жасау функциясы
def get_or_create_player(username):
    conn = get_db_connection() # Қосылуды орнату
    cur = conn.cursor()        # SQL командаларын орындау үшін "курсор" ашу
    
    # Ойыншыны қосу. Егер мұндай ат бар болса (ON CONFLICT), ештеңе істемеу (DO NOTHING)
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    
    # Ойыншының ID-ін алу
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player_id = cur.fetchone()[0] # Бірінші табылған ID-ді айнымалыға сақтау
    
    conn.commit()  # Өзгерістерді деректер қорында бекіту (сақтау)
    cur.close()    # Курсорды жабу
    conn.close()   # Байланысты үзу
    return player_id

# Ойын сессиясын (нәтижені) сақтау
def save_game_session(player_id, score, level):
    conn = get_db_connection()
    cur = conn.cursor()
    # Ойыншының ID-і, жинаған ұпайы мен жеткен деңгейін кестеге жазу
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

# Ең үздік 10 нәтижені алу
def get_top_10():
    conn = get_db_connection()
    cur = conn.cursor()
    # "JOIN" арқылы екі кестені (players және game_sessions) біріктіріп, 
    # ұпайы бойынша кему ретімен (DESC) алғашқы 10-ын таңдап алу
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at 
        FROM game_sessions gs 
        JOIN players p ON gs.player_id = p.id 
        ORDER BY gs.score DESC LIMIT 10
    """)
    res = cur.fetchall() # Барлық табылған қатарларды тізім қылып алу
    cur.close()
    conn.close()
    return res

# Ойыншының жеке рекордын алу
def get_personal_best(player_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # MAX(score) - берілген ID бойынша ең жоғарғы ұпайды табу
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    # Егер нәтиже болса соны, болмаса 0-ді қайтару
    return res if res else 0