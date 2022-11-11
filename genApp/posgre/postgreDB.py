import psycopg2


def connectionTest(request):
    try:
        connect = psycopg2.connect(host='localhost', port='5432', dbname='postgres', user='postgres',
                                   password='비밀번호')
        connect.close()
        return True
    except:
        return False

def connection(request):
    return psycopg2.connect(host='localhost', port='5432', dbname='postgres', user='postgres',
                                   password='비밀번호')


def close(cursor, conn):
    # 객체 닫기
    cursor.close()
    # 서버와 연결 끊기
    conn.close()
