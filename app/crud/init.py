import logging
import pymysql
from fastapi import HTTPException

from app.db.connect import (
    close_connection,
    close_cursor,
    get_db_connection,
    get_re_db_connection
)
import uuid


def get_or_create_store_uuid(store_business_id: str) -> str:
    conn = get_re_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ 이미 UUID가 있는지 조회
        select_query = """
            SELECT uuid FROM store_uuid WHERE store_business_id = %s
        """
        cursor.execute(select_query, (store_business_id,))
        result = cursor.fetchone()

        if result:
            return result[0]  # 기존 UUID 반환

        # 2️⃣ 없으면 UUID 생성해서 저장
        new_uuid = str(uuid.uuid4())
        insert_query = """
            INSERT INTO store_uuid (store_business_id, uuid)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (store_business_id, new_uuid))
        conn.commit()

        return new_uuid

    except Exception as e:
        logging.error(f"DB 오류: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail="DB 처리 중 오류 발생")

    finally:
        close_cursor(cursor)
        close_connection(conn)



def get_uuid_store(uuid: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ 이미 UUID가 있는지 조회
        select_query = """
            SELECT store_business_id FROM store_uuid WHERE uuid = %s
        """
        cursor.execute(select_query, (uuid,))
        result = cursor.fetchone()

        return result[0]  # 기존 UUID 반환

        

    except Exception as e:
        logging.error(f"DB 오류: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail="DB 처리 중 오류 발생")

    finally:
        close_cursor(cursor)
        close_connection(conn)