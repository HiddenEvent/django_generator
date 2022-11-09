from genApp import mysqlDB
from django.shortcuts import render


# Create your views here.



def home(request):
    isSuccess = mysqlDB.connectionTest(request)
    if not isSuccess:
        print("mysql DB connection 실패")

    conn = mysqlDB.connection(request)
    cursor = conn.cursor(dictionary=True)
    try:
        strSql = '''SELECT DISTINCT TABLE_SCHEMA AS SCHEMA_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_SCHEMA NOT IN ('information_schema','performance_schema');
                    '''
        result = cursor.execute(strSql)
        users = cursor.fetchall()

        conn.commit()
        conn.close()

    except:
        conn.rollback()
        print("스키마 정보 조회 실패")

    mysqlDB.close(cursor, conn)

    return render(request, 'home.html')
