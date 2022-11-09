import mysql.connector


def connectionTest(request):
    try:
        connect = mysql.connector.connect(host='localhost', port='3306', database='public', user='richardkim',
                                          password='비밀번호')
        return True
    except:
        return False

def connection(request):
    return mysql.connector.connect(host='localhostg', port='3306', database='public', user='richardkim',
                                      password='비밀번호')


def close(cursor, conn):
    # 객체 닫기
    cursor.close()
    # 서버와 연결 끊기
    conn.close
