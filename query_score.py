import sqlite3, os

db_name = 'snake_score'
tab_name = 'score'

def gen_table():
    conn = sqlite3.connect("{}.db".format(db_name))
    c = conn.cursor()
    c.execute("""CREATE TABLE {} (
        playername text,                         
        scr integer
        )""".format(tab_name))
    print("Table Created")
    conn.commit()
    conn.close()

def query():
    conn = sqlite3.connect("{}.db".format(db_name))
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(tab_name))
    tab_all = c.fetchall()
    for line in tab_all:
        print(line[0] + "\t" + str(line[1]))
    print("Query completed.")
    conn.commit()
    conn.close()

def order_results():
    conn = sqlite3.connect("{}.db".format(db_name))
    c = conn.cursor()
    c.execute("SELECT scr, * FROM {} ORDER BY scr DESC".format(tab_name))
    tab_all = c.fetchall()
    for line in tab_all:
        print(line)
    print("Table Ordered.")
    conn.commit()
    conn.close()

#gen_table()
os.system('python snake.py')
order_results()

