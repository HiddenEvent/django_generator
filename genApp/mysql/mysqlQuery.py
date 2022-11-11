## 1. 전체 스키마명 조회 (기본스키마 제외)
def ALL_SCHEMA(cursor):
    cursor.execute("""
    SELECT DISTINCT
        TABLE_SCHEMA AS SCHEMA_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA NOT IN ('information_schema','performance_schema')
    """)  # SQL 문장 실행
    return cursor.fetchall()

## 2. 전체 테이블 명 + 코멘트 조회
def ALL_TABLE_INFO(cursor, schemaName):
    cursor.execute("""
    SELECT
        TABLE_SCHEMA AS SCHEMA_NAME,
        TABLE_NAME AS TABLE_NAME,
        TABLE_COMMENT AS TABLE_COMMENT
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = """+schemaName+"""
    """)  # SQL 문장 실행
    return cursor.fetchall()

## 3. 선택한 테이블 -> 모든 컬럼 + 코멘트 조회 + 키종류 + FK 테이블 정보
def ALL_COLUMN_INFO(cursor, schemaName, tableName):
    cursor.execute("""
    SELECT DISTINCT
        COL.ORDINAL_POSITION AS ORD_NUM,
        CASE COL.COLUMN_KEY
            WHEN 'PRI'
                THEN 'PK'
            WHEN 'MUL'
                THEN 'FK'
        END KEY_TYPE,
        COL.TABLE_NAME AS TABLE_NAME,
        COL.COLUMN_NAME AS COLUMN_NAME,
        COL.COLUMN_COMMENT AS COLUMN_COMMENT,
        COL.DATA_TYPE AS COLUMN_TYPE,
        COL.CHARACTER_MAXIMUM_LENGTH AS COLUMN_LENGTH,
        COL.IS_NULLABLE AS IS_NULLABLE,
        COL.COLUMN_DEFAULT AS COLUMN_DEFAULT_VALUE,
        KCU.REFERENCED_TABLE_NAME AS REF_TABLE_NAME,
        KCU.REFERENCED_COLUMN_NAME AS REF_COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS COL
    LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU
        ON COL.TABLE_SCHEMA = KCU.TABLE_SCHEMA
        AND COL.TABLE_NAME = KCU.TABLE_NAME
        AND COL.COLUMN_NAME = KCU.COLUMN_NAME
    WHERE COL.TABLE_SCHEMA = """+schemaName+"""
        AND COL.TABLE_NAME = """+tableName+"""
    ORDER BY COL.ORDINAL_POSITION
    """)  # SQL 문장 실행
    return cursor.fetchall()
