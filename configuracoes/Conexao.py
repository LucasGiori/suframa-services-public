import psycopg2


def newConnection():
    try :
        conn = psycopg2.connect(database="simnac", user="postgres", password="lucas770", host="127.0.0.1", port="5432")
        cursor = conn.cursor()
        return conn,cursor
    except Exception as e :
        print("[!] ",e)
        
def stopConnection(conn):
    conn.close()
