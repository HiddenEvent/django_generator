## 1. 전체 스키마명 조회 (기본스키마 제외)
def ALL_SCHEMA(cursor):
    cursor.execute("""
    SELECT DISTINCT
        N.NSPNAME AS SCHEMA_NAME
    FROM PG_CATALOG.PG_CLASS C
        INNER JOIN PG_CATALOG.PG_NAMESPACE N ON C.RELNAMESPACE=N.OID
    WHERE C.RELKIND = 'r'
    AND NSPNAME NOT IN ('pg_catalog','information_schema')
    """)  # SQL 문장 실행
    return cursor.fetchall()

## 2. 전체 테이블 명 + 코멘트 조회
def ALL_TABLE_INFO(cursor, schemaName):
    cursor.execute("""
    SELECT
        N.NSPNAME AS SCHEMA_NAME,
        C.RELNAME AS TABLE_NAME,
        OBJ_DESCRIPTION(C.OID) AS TABLE_COMMENT
    FROM PG_CATALOG.PG_CLASS C
        INNER JOIN PG_CATALOG.PG_NAMESPACE N ON C.RELNAMESPACE=N.OID
    WHERE C.RELKIND = 'r'
    AND NSPNAME =  """+schemaName+"""
    ORDER BY C.OID;
    """)  # SQL 문장 실행
    return cursor.fetchall()

## 3. 선택한 테이블 -> 모든 컬럼 + 코멘트 조회 + 키종류 + FK 테이블 정보
def ALL_COLUMN_INFO(cursor, schemaName, tableName):
    cursor.execute("""
    SELECT
        ISC.ordinal_position AS ORD_NUM,
        CASE KEY_INFO.KEY_TYPE
            WHEN 'PRIMARY KEY'
                THEN 'PK'
            WHEN 'FOREIGN KEY'
                THEN 'FK'
        END KEY_TYPE,
        PS.RELNAME AS TABLE_NAME,
        ISC.column_name AS COLUMN_NAME,
        PD.DESCRIPTION AS COLUMN_COMMENT,
        ISC.udt_name AS COLUMN_TYPE,
        ISC.character_maximum_length AS COLUMN_LENGTH,
        ISC.is_nullable AS IS_NULLABLE,
        ISC.column_default AS COLUMN_DEFAULT_VALUE,
        CASE KEY_INFO.KEY_TYPE
            WHEN 'FOREIGN KEY'
                THEN KEY_INFO.TABLE_NAME
        END REF_TABLE_NAME,
        CASE KEY_INFO.KEY_TYPE
            WHEN 'FOREIGN KEY'
                THEN KEY_INFO.COLUMN_NAME
        END REF_COLUMN_NAME
    FROM PG_STAT_ALL_TABLES PS
        JOIN PG_DESCRIPTION PD ON PS.RELID=PD.OBJOID
            AND PS.SCHEMANAME="""+schemaName+"""/*스키마 명*/
            AND PS.RELNAME="""+tableName+"""/*테이블 명*/
        JOIN PG_ATTRIBUTE PA ON PD.OBJOID=PA.ATTRELID
            AND PD.OBJSUBID=PA.ATTNUM
            AND PD.OBJSUBID<>0
        JOIN INFORMATION_SCHEMA.COLUMNS ISC ON ISC.COLUMN_NAME =PA.ATTNAME
            AND ISC.TABLE_SCHEMA = """+schemaName+"""
            AND ISC.TABLE_NAME = """+tableName+"""
        LEFT JOIN (SELECT
                        TC.constraint_type AS KEY_TYPE,
                        TC.table_name AS FK_TABLE_NAME,
                        KCU.column_name AS FK_COLUMN_NAME,
                        CCU.table_name AS TABLE_NAME,
                        CCU.column_name AS COLUMN_NAME
                    FROM information_schema.table_constraints TC
                    JOIN information_schema.key_column_usage KCU /*현재 테이블*/ ON KCU.constraint_name = TC.constraint_name
                    JOIN information_schema.constraint_column_usage CCU /*타겟 테이블*/ ON CCU.constraint_name = TC.constraint_name
                    WHERE
                        TC.constraint_schema="""+schemaName+""" /*스키마 명*/
                        AND TC.table_name="""+tableName+""" /*테이블 명*/) KEY_INFO ON KEY_INFO.FK_COLUMN_NAME= ISC.COLUMN_NAME
    ORDER BY ORD_NUM
    """)  # SQL 문장 실행
    return cursor.fetchall()
