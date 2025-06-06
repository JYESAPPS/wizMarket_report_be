import logging
import pymysql
from fastapi import HTTPException

from app.db.connect import (
    close_connection,
    close_cursor,
    get_db_connection,
)
from app.schemas.report import (
    LocalStoreCDCommercialDistrict,
    LocalStoreCDDistrictAverageSalesTop5,
    LocalStoreCDJSWeightedAverage,
    LocalStoreCDTiemAverageSalesPercent,
    LocalStoreCDWeekdayAverageSalesPercent,
    LocalStoreCommercialDistrictJscoreAverage,
    LocalStoreMainCategoryCount,
    LocalStoreTop5Menu,
)

logger = logging.getLogger(__name__)


def select_rising_menu_top5_by_store_business_number(
    store_business_id: str,
) -> LocalStoreTop5Menu:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT
                        CITY_NAME,
                        DISTRICT_NAME,
                        SUB_DISTRICT_NAME,
                        DETAIL_CATEGORY_NAME,
                        DETAIL_CATEGORY_TOP1_ORDERED_MENU,
                        DETAIL_CATEGORY_TOP2_ORDERED_MENU,
                        DETAIL_CATEGORY_TOP3_ORDERED_MENU,
                        DETAIL_CATEGORY_TOP4_ORDERED_MENU,
                        DETAIL_CATEGORY_TOP5_ORDERED_MENU
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                    ;
                """

                # logger.info(f"Executing query: {select_query}")
                cursor.execute(select_query, (store_business_id,))

                row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreTop5Menu {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                result = LocalStoreTop5Menu(
                    city_name=row["CITY_NAME"],
                    district_name=row["DISTRICT_NAME"],
                    sub_district_name=row["SUB_DISTRICT_NAME"],
                    detail_category_name=row["DETAIL_CATEGORY_NAME"],
                    detail_category_top1_ordered_menu=row[
                        "DETAIL_CATEGORY_TOP1_ORDERED_MENU"
                    ],
                    detail_category_top2_ordered_menu=row[
                        "DETAIL_CATEGORY_TOP2_ORDERED_MENU"
                    ],
                    detail_category_top3_ordered_menu=row[
                        "DETAIL_CATEGORY_TOP3_ORDERED_MENU"
                    ],
                    detail_category_top4_ordered_menu=row[
                        "DETAIL_CATEGORY_TOP4_ORDERED_MENU"
                    ],
                    detail_category_top5_ordered_menu=row[
                        "DETAIL_CATEGORY_TOP5_ORDERED_MENU"
                    ],
                )

                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error occurred LocalStoreTop5Menu: {str(e)}")
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")


def select_c_d_j_score_average_by_store_business_number(
    store_business_id: str,
) -> LocalStoreCDJSWeightedAverage:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT 
                        COMMERCIAL_DISTRICT_J_SCORE_AVERAGE
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                    ;
                """

                # logger.info(
                #     f"Executing query: {select_query} with business ID: {store_business_id}"
                # )
                cursor.execute(select_query, (store_business_id,))

                row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreCDJSWeightedAverage {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                result = LocalStoreCDJSWeightedAverage(
                    commercial_district_j_score_average=round(
                        row.get("COMMERCIAL_DISTRICT_J_SCORE_AVERAGE") or 0, 1
                    ),
                )

                # logger.info(f"Result for business ID {store_business_id}: {result}")
                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in select_c_d_j_score_average_by_store_business_number: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")


def select_c_d_main_category_count_by_store_business_number(
    store_business_id: str,
) -> LocalStoreMainCategoryCount:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT 
                        COMMERCIAL_DISTRICT_FOOD_BUSINESS_COUNT,
                        COMMERCIAL_DISTRICT_HEALTHCARE_BUSINESS_COUNT,
                        COMMERCIAL_DISTRICT_EDUCATION_BUSINESS_COUNT,
                        COMMERCIAL_DISTRICT_ENTERTAINMENT_BUSINESS_COUNT,
                        COMMERCIAL_DISTRICT_LIFESTYLE_BUSINESS_COUNT,
                        COMMERCIAL_DISTRICT_RETAIL_BUSINESS_COUNT
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                    ;
                """

                # logger.info(
                #     f"Executing query: {select_query} with business ID: {store_business_id}"
                # )
                cursor.execute(select_query, (store_business_id,))

                row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreMainCategoryCount {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                result = LocalStoreMainCategoryCount(
                    commercial_district_food_business_count=row.get(
                        "COMMERCIAL_DISTRICT_FOOD_BUSINESS_COUNT"
                    ),
                    commercial_district_healthcare_business_count=row.get(
                        "COMMERCIAL_DISTRICT_HEALTHCARE_BUSINESS_COUNT"
                    ),
                    commercial_district_education_business_count=row.get(
                        "COMMERCIAL_DISTRICT_EDUCATION_BUSINESS_COUNT"
                    ),
                    commercial_district_entertainment_business_count=row.get(
                        "COMMERCIAL_DISTRICT_ENTERTAINMENT_BUSINESS_COUNT"
                    ),
                    commercial_district_lifestyle_business_count=row.get(
                        "COMMERCIAL_DISTRICT_LIFESTYLE_BUSINESS_COUNT"
                    ),
                    commercial_district_retail_business_count=row.get(
                        "COMMERCIAL_DISTRICT_RETAIL_BUSINESS_COUNT"
                    ),
                )

                # logger.info(f"Result for business ID {store_business_id}: {result}")
                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in select_c_d_main_category_count_by_store_business_number: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")


def select_commercial_district_j_score_by_store_business_number(
    store_business_id: str,
) -> LocalStoreCommercialDistrictJscoreAverage:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT 
                        COMMERCIAL_DISTRICT_MARKET_SIZE_J_SCORE,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_J_SCORE,
                        COMMERCIAL_DISTRICT_USAGE_COUNT_J_SCORE,
                        COMMERCIAL_DISTRICT_SUB_DISTRICT_DENSITY_J_SCORE,
                        COMMERCIAL_DISTRICT_AVERAGE_PAYMENT_J_SCORE
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                    ;
                """

                # logger.info(
                #     f"Executing query: {select_query} with business ID: {store_business_id}"
                # )
                cursor.execute(select_query, (store_business_id,))

                row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreCommercialDistrictJscoreAverage {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                result = LocalStoreCommercialDistrictJscoreAverage(
                    commercial_district_market_size_j_socre=round(
                        row.get("COMMERCIAL_DISTRICT_MARKET_SIZE_J_SCORE") or 0, 1
                    ),
                    commercial_district_average_sales_j_socre=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_J_SCORE") or 0, 1
                    ),
                    commercial_district_usage_count_j_socre=round(
                        row.get("COMMERCIAL_DISTRICT_USAGE_COUNT_J_SCORE") or 0, 1
                    ),
                    commercial_district_sub_district_density_j_socre=round(
                        row.get("COMMERCIAL_DISTRICT_SUB_DISTRICT_DENSITY_J_SCORE")
                        or 0,
                        1,
                    ),
                    commercial_district_sub_average_payment_j_socre=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_PAYMENT_J_SCORE") or 0, 1
                    ),
                )

                # logger.info(f"Result for business ID {store_business_id}: {result}")
                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in select_commercial_district_j_score_by_store_business_number: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")


def select_commercial_district_weekday_average_sales_by_store_business_number(
    store_business_id: str,
) -> LocalStoreCDWeekdayAverageSalesPercent:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT 
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_MON,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_TUE,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_WED,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_THU,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_FRI,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SAT,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SUN
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                    ;
                """

                # logger.info(
                #     f"Executing query: {select_query} with business ID: {store_business_id}"
                # )
                cursor.execute(select_query, (store_business_id,))

                row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreCDWeekdayAverageSalesPercent {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                result = LocalStoreCDWeekdayAverageSalesPercent(
                    commercial_district_average_sales_percent_mon=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_MON") or 0, 1
                    ),
                    commercial_district_average_sales_percent_tue=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_TUE") or 0, 1
                    ),
                    commercial_district_average_sales_percent_wed=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_WED") or 0, 1
                    ),
                    commercial_district_average_sales_percent_thu=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_THU") or 0, 1
                    ),
                    commercial_district_average_sales_percent_fri=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_FRI") or 0, 1
                    ),
                    commercial_district_average_sales_percent_sat=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SAT") or 0, 1
                    ),
                    commercial_district_average_sales_percent_sun=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SUN") or 0, 1
                    ),
                )

                # logger.info(f"Result for business ID {store_business_id}: {result}")
                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in select_commercial_district_weekday_average_sales_by_store_business_number: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")


def select_commercial_district_time_average_sales_by_store_business_number(
    store_business_id: str,
) -> LocalStoreCDTiemAverageSalesPercent:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT 
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_06_09,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_09_12,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_12_15,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_15_18,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_18_21,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_21_24
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SUN
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                    ;
                """

                # logger.info(
                #     f"Executing query: {select_query} with business ID: {store_business_id}"
                # )
                cursor.execute(select_query, (store_business_id,))

                row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreCDTiemAverageSalesPercent {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                result = LocalStoreCDTiemAverageSalesPercent(
                    commercial_district_average_sales_percent_06_09=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_06_09") or 0,
                        1,
                    ),
                    commercial_district_average_sales_percent_09_12=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_09_12") or 0,
                        1,
                    ),
                    commercial_district_average_sales_percent_12_15=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_12_15") or 0,
                        1,
                    ),
                    commercial_district_average_sales_percent_15_18=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_15_18") or 0,
                        1,
                    ),
                    commercial_district_average_sales_percent_18_21=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_18_21") or 0,
                        1,
                    ),
                    commercial_district_average_sales_percent_21_24=round(
                        row.get("COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_21_24") or 0,
                        1,
                    ),
                )

                # logger.info(f"Result for business ID {store_business_id}: {result}")
                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in select_commercial_district_time_average_sales_by_store_business_number: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")


def select_commercial_district_rising_sales_by_store_business_number(
    store_business_id: str,
) -> LocalStoreCDDistrictAverageSalesTop5:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT 
                        COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP1_INFO,
                        COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP2_INFO,
                        COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP3_INFO,
                        COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP4_INFO,
                        COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP5_INFO
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                    ;
                """

                # logger.info(
                #     f"Executing query: {select_query} with business ID: {store_business_id}"
                # )

                cursor.execute(select_query, (store_business_id,))

                row = cursor.fetchone()

                # logger.info(f"row: {row} with business ID: {store_business_id}")

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreCDDistrictAverageSalesTop5 {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                result = LocalStoreCDDistrictAverageSalesTop5(
                    commercial_district_detail_category_average_sales_top1_info=(
                        row.get(
                            "COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP1_INFO"
                        )
                    ),
                    commercial_district_detail_category_average_sales_top2_info=row.get(
                        "COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP2_INFO"
                    ),
                    commercial_district_detail_category_average_sales_top3_info=row.get(
                        "COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP3_INFO"
                    ),
                    commercial_district_detail_category_average_sales_top4_info=row.get(
                        "COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP4_INFO"
                    ),
                    commercial_district_detail_category_average_sales_top5_info=row.get(
                        "COMMERCIAL_DISTRICT_DETAIL_CATEGORY_AVERAGE_SALES_TOP5_INFO"
                    ),
                )

                # logger.info(f"Result for business ID {store_business_id}: {result}")
                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in select_commercial_district_rising_sales_by_store_business_number: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")


# 상권분석 읍/면/동 소분류 상권분석
def select_commercial_district_commercial_district_by_store_business_number(
    store_business_id: str,
) -> LocalStoreCDCommercialDistrict:

    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                select_query = """
                    SELECT 
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_MON,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_TUE,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_WED,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_THU,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_FRI,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SAT,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SUN,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_06_09,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_09_12,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_12_15,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_15_18,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_18_21,
                        COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_21_24,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_20S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_30S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_40S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_50S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_60_over,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_20S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_30S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_40S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_50S,
                        COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_60_over,
                        COMMERCIAL_DISTRICT_NATIONAL_DENSITY_AVERAGE,
                        COMMERCIAL_DISTRICT_SUB_DISTRICT_DENSITY_AVERAGE,
                        COMMERCIAL_DISTRICT_NATIONAL_AVERAGE_SALES,
                        COMMERCIAL_DISTRICT_SUB_DISTRICT_AVERAGE_SALES,
                        COMMERCIAL_DISTRICT_NATIONAL_AVERAGE_PAYMENT,
                        COMMERCIAL_DISTRICT_SUB_DISTRICT_AVERAGE_PAYMENT,
                        COMMERCIAL_DISTRICT_NATIONAL_USAGE_COUNT,
                        COMMERCIAL_DISTRICT_SUB_DISTRICT_USAGE_COUNT
                    FROM
                        REPORT 
                    WHERE STORE_BUSINESS_NUMBER = %s
                """

                cursor.execute(select_query, (store_business_id,))
                row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404,
                        detail=f"LocalStoreCDCommercialDistrict {store_business_id}에 해당하는 매장 정보를 찾을 수 없습니다.",
                    )

                # 주요 고객 비율 비교 (예: 최고 비율 2개 찾기)
                age_gender_mapping = {
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_20S": "20대 남성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_30S": "30대 남성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_40S": "40대 남성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_50S": "50대 남성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_M_60_over": "60대 이상 남성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_20S": "20대 여성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_30S": "30대 여성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_40S": "40대 여성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_50S": "50대 여성",
                    "COMMERCIAL_DISTRICT_AVG_CLIENT_PER_F_60_over": "60대 이상 여성",
                }

                # 주요 고객 비율 중 최고 2개 추출
                sorted_client_data = sorted(
                    (
                        (k, v)
                        for k, v in row.items()
                        if k in age_gender_mapping and v is not None
                    ),
                    key=lambda item: item[1] or 0,  # None일 경우 0으로 처리
                    reverse=True,
                )

                top1 = (
                    sorted_client_data[0] if len(sorted_client_data) > 0 else (None, 0)
                )
                top2 = (
                    sorted_client_data[1] if len(sorted_client_data) > 1 else (None, 0)
                )

                # 요일별 최대 및 최소 판매 비율 찾기
                weekdays = [
                    ("월요일", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_MON"]),
                    ("화요일", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_TUE"]),
                    ("수요일", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_WED"]),
                    ("목요일", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_THU"]),
                    ("금요일", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_FRI"]),
                    ("토요일", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SAT"]),
                    ("일요일", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_SUN"]),
                ]

                # None이거나 0인 경우 필터링
                weekdays_filtered = [
                    (day, percent)
                    for day, percent in weekdays
                    if percent is not None and percent != 0
                ]

                max_weekday = (
                    max(weekdays_filtered, key=lambda x: x[1])
                    if weekdays_filtered
                    else ("-", 0)
                )
                min_weekday = (
                    min(weekdays_filtered, key=lambda x: x[1])
                    if weekdays_filtered
                    else ("-", 0)
                )

                # 시간대별 최대 판매 비율 찾기
                time_slots = [
                    ("06~09", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_06_09"]),
                    ("09~12", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_09_12"]),
                    ("12~15", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_12_15"]),
                    ("15~18", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_15_18"]),
                    ("18~21", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_18_21"]),
                    ("21~24", row["COMMERCIAL_DISTRICT_AVERAGE_SALES_PERCENT_21_24"]),
                ]

                # None이거나 0인 경우 필터링
                time_slots_filtered = [
                    (slot, percent)
                    for slot, percent in time_slots
                    if percent is not None and percent != 0
                ]

                max_time = (
                    max(time_slots_filtered, key=lambda x: x[1])
                    if time_slots_filtered
                    else ("-", 0)
                )

                # LocalStoreCDCommercialDistrict 인스턴스 생성 및 값 할당
                result = LocalStoreCDCommercialDistrict(
                    commercial_district_national_density_average=row.get(
                        "COMMERCIAL_DISTRICT_NATIONAL_DENSITY_AVERAGE", 0.0
                    ),
                    commercial_district_sub_district_density_average=row.get(
                        "COMMERCIAL_DISTRICT_SUB_DISTRICT_DENSITY_AVERAGE", 0.0
                    ),
                    commercial_district_national_average_sales=row.get(
                        "COMMERCIAL_DISTRICT_NATIONAL_AVERAGE_SALES"
                    )
                    or 0,
                    commercial_district_sub_district_average_sales=row.get(
                        "COMMERCIAL_DISTRICT_SUB_DISTRICT_AVERAGE_SALES"
                    )
                    or 0,
                    commercial_district_national_average_payment=row.get(
                        "COMMERCIAL_DISTRICT_NATIONAL_AVERAGE_PAYMENT"
                    )
                    or 0,
                    commercial_district_sub_district_average_payment=row.get(
                        "COMMERCIAL_DISTRICT_SUB_DISTRICT_AVERAGE_PAYMENT"
                    )
                    or 0,
                    commercial_district_national_usage_count=row.get(
                        "COMMERCIAL_DISTRICT_NATIONAL_USAGE_COUNT"
                    )
                    or 0,
                    commercial_district_sub_district_usage_count=row.get(
                        "COMMERCIAL_DISTRICT_SUB_DISTRICT_USAGE_COUNT"
                    )
                    or 0,
                    commercial_district_average_sales_max_percent_client_top1=age_gender_mapping.get(
                        top1[0], "-"
                    ),
                    commercial_district_average_sales_max_percent_client_top2=age_gender_mapping.get(
                        top2[0], "-"
                    ),
                    commercial_district_average_sales_max_percent_weekday=max_weekday[
                        0
                    ],
                    commercial_district_average_sales_min_percent_weekday=min_weekday[
                        0
                    ],
                    commercial_district_average_sales_max_percent_time=max_time[0],
                )

                return result

    except pymysql.Error as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=f"데이터베이스 연결 오류: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error in select_commercial_district_commercial_district_by_store_business_number: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")
