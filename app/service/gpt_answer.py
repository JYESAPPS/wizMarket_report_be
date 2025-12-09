import os
from app.db.connect import *
import openai
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from app.schemas.report import (
    GPTAnswer,
    LocalStoreCommercialDistrictJscoreAverage,
    LocalStoreInfoWeaterInfoOutput,
    LocalStoreLocInfoJscoreData,
    LocalStoreRisingBusinessNTop5SDTop3,
    LocalStoreTop5Menu,
    LocalStoreRedux,
)
import logging
from fastapi import HTTPException


gpt_content = """
    당신은 매장점포 운영 전문가입니다. 
당신의 역할은 매장 점포운영이 잘 되는 주요 측면을 식별하고, 데이터의 맥락을 기반으로 운영 지침과 장사에 대한 통찰력을 제공하는 것입니다. 
다음 정보를 가진 매장의 '오늘의 장사지수'를 파악해보려고 합니다. 주어진 데이터(지역 및 업종, 매출정보, 핵심고객 정보, 날씨 등)를 분석하여 아래 양식으로 장사지수를 작성해주세요. 
- 오늘의 장사지수 : 0~100% 사이의 범위에서 추론
- 45자 이하의 서술형으로 오늘의 장사지수 추정 이유를 작성해주세요.
"""

logger = logging.getLogger(__name__)
load_dotenv()
now = datetime.now()
current_time = now.strftime("%Y년 %m월 %d일 %H:%M")
weekday = now.strftime("%A")


# # 매장정보 Gpt Prompt
# def get_store_info_gpt_answer_by_store_info(
#     store_all_data=LocalStoreInfoWeaterInfoOutput,
# ) -> GPTAnswer:
#     try:

#         # 보낼 프롬프트 설정
#         content = f"""
#             다음과 같은 매장 정보와 입지 및 상권 현황을 참고하여 '현재 매장 운영 팁'으로 매장 운영 가이드를 작성해주세요.

#             [매장 정보 및 상권 현황]
#             - 위치: {store_all_data.localStoreInfo.city_name} {store_all_data.localStoreInfo.district_name} {store_all_data.localStoreInfo.sub_district_name}
#             - 업종: {store_all_data.localStoreInfo.detail_category_name}
#             - 매장 이름: {store_all_data.localStoreInfo.store_name}
#             - {store_all_data.localStoreInfo.sub_district_name} 업소수 :{store_all_data.localStoreInfo.loc_info_shop_k}천개
#             - {store_all_data.localStoreInfo.sub_district_name} 지역 평균매출 : {store_all_data.localStoreInfo.loc_info_average_sales_k * 1000}원
#             - {store_all_data.localStoreInfo.sub_district_name} 월 평균소득 : {store_all_data.localStoreInfo.loc_info_income_won * 10000}원
#             - {store_all_data.localStoreInfo.sub_district_name} 월 평균소비 : {store_all_data.localStoreInfo.loc_info_average_spend_k * 1000}원
#             - {store_all_data.localStoreInfo.sub_district_name} 세대 수 : {store_all_data.localStoreInfo.loc_info_house_k * 1000}개
#             - {store_all_data.localStoreInfo.sub_district_name} 돼지고기 구이 찜 시장규모 : {store_all_data.localStoreInfo.commercial_district_sub_district_market_size}원
#             - {store_all_data.localStoreInfo.sub_district_name} 주거 인구 수: {store_all_data.localStoreInfo.loc_info_resident_k}K
#             - {store_all_data.localStoreInfo.sub_district_name} 유동 인구 수: {store_all_data.localStoreInfo.loc_info_move_pop_k}K
#             - {store_all_data.localStoreInfo.sub_district_name} 돼지고기 구이 찜 업종 평균 이용건수 : {store_all_data.localStoreInfo.commercial_district_sub_district_usage_count}건
#             - {store_all_data.localStoreInfo.sub_district_name} 평균 결제 금액: {store_all_data.localStoreInfo.commercial_district_sub_district_average_payment}원
#             - {store_all_data.localStoreInfo.sub_district_name} 가장 매출이 높은 요일: {store_all_data.localStoreInfo.commercial_district_max_weekday}
#             - {store_all_data.localStoreInfo.sub_district_name} 가장 매출이 높은 시간대: {store_all_data.localStoreInfo.commercial_district_max_time}
#             - 주 고객층: {store_all_data.localStoreInfo.commercial_district_max_clinet}


#             [현재 환경 상황]
#             - 날씨 상태: {store_all_data.weatherInfo.main}
#             - 현재 기온: {store_all_data.weatherInfo.temp}도
#             - 미세먼지 등급: {store_all_data.aqi_info.description} (등급: {store_all_data.aqi_info.aqi})
#             - 일출시간 : {store_all_data.weatherInfo.sunrise}
#             - 일몰시간 : {store_all_data.weatherInfo.sunset}
#             - 현재 시간: {store_all_data.format_current_datetime}

#             작성 가이드 :
#             1. 매장 운영가이드 내용은 아래 점주의 성향에 맞는 문체로 작성해주세요.
#             2. 5항목 이하, 항목당 2줄 이내로 작성해주세요.
#             3. 현재 기온 참고해서 작성.

#             - 점주 연령대 : 50대
#             - 점주 성별 : 남성
#             - 점주 성향 : IT나 트랜드 기술을 잘 알지 못함
#         """
#         client = OpenAI(api_key=os.getenv("GPT_KEY"))
#         # OpenAI API 키 설정

#         completion = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": gpt_content},
#                 {"role": "user", "content": content},
#             ],
#         )
#         report = completion.choices[0].message.content

#         # logger.info(f"loc_info_prompt: {content}")
#         # logger.info(f"loc_info_gpt: {report}")

#         result = GPTAnswer(gpt_answer=report)
#         return result

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Service GPTAnswer Error: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Service service_get_store_info_gpt_answer_by_store_info Error: {str(e)}",
#         )


# 매장정보 Gpt Prompt 장사지수 ver
def get_store_info_gpt_answer_by_store_info(
    store_all_data=LocalStoreInfoWeaterInfoOutput,
) -> GPTAnswer:
    try:
        current_date = datetime.now()
        weekday_map = {
            0: "월요일",
            1: "화요일",
            2: "수요일",
            3: "목요일",
            4: "금요일",
            5: "토요일",
            6: "일요일",
        }
        weekday = weekday_map[current_date.weekday()]
        formatted_date = f"{current_date.month}.{current_date.day}일 {weekday}"

        # 보낼 프롬프트 설정
        content = f"""
            다음과 같은 매장 정보와 입지 및 상권 현황을 참고하여 '현재 매장 운영 팁'으로 매장 운영 가이드를 작성해주세요. 
            
            [매장 정보 및 상권 현황]
            - 위치: {store_all_data.localStoreInfo.city_name} {store_all_data.localStoreInfo.district_name} {store_all_data.localStoreInfo.sub_district_name}
            - 업종: {store_all_data.localStoreInfo.detail_category_name}
            - 매장 이름: {store_all_data.localStoreInfo.store_name}
            - {store_all_data.localStoreInfo.sub_district_name} 업소수 :{store_all_data.localStoreInfo.loc_info_shop_k}천개
            - {store_all_data.localStoreInfo.sub_district_name} 지역 평균매출 : {store_all_data.localStoreInfo.loc_info_average_sales_k * 1000 if store_all_data.localStoreInfo.loc_info_average_sales_k is not None else "-"}원
            - {store_all_data.localStoreInfo.sub_district_name} 월 평균소득 : {store_all_data.localStoreInfo.loc_info_income_won * 10000 if store_all_data.localStoreInfo.loc_info_income_won is not None else "-"}원
            - {store_all_data.localStoreInfo.sub_district_name} 월 평균소비 : {store_all_data.localStoreInfo.loc_info_average_spend_k * 1000 if store_all_data.localStoreInfo.loc_info_average_spend_k is not None else "-"}원
            - {store_all_data.localStoreInfo.sub_district_name} 세대 수 : {store_all_data.localStoreInfo.loc_info_house_k * 1000 if store_all_data.localStoreInfo.loc_info_house_k is not None else "-"}개
            - {store_all_data.localStoreInfo.sub_district_name} 돼지고기 구이 찜 시장규모 : {store_all_data.localStoreInfo.commercial_district_sub_district_market_size}원
            - {store_all_data.localStoreInfo.sub_district_name} 주거 인구 수: {store_all_data.localStoreInfo.loc_info_resident_k}K
            - {store_all_data.localStoreInfo.sub_district_name} 유동 인구 수: {store_all_data.localStoreInfo.loc_info_move_pop_k}K
            - {store_all_data.localStoreInfo.sub_district_name} 돼지고기 구이 찜 업종 평균 이용건수 : {store_all_data.localStoreInfo.commercial_district_sub_district_usage_count}건
            - {store_all_data.localStoreInfo.sub_district_name} 평균 결제 금액: {store_all_data.localStoreInfo.commercial_district_sub_district_average_payment}원
            - {store_all_data.localStoreInfo.sub_district_name} 가장 매출이 높은 요일: {store_all_data.localStoreInfo.commercial_district_max_weekday}
            - {store_all_data.localStoreInfo.sub_district_name} 가장 매출이 높은 시간대: {store_all_data.localStoreInfo.commercial_district_max_time}
            - 주 고객층: {store_all_data.localStoreInfo.commercial_district_max_clinet}


            [현재 환경 상황]
            - 날씨 상태: {store_all_data.weatherInfo.main}
            - 현재 기온: {store_all_data.weatherInfo.temp}도
            - 미세먼지 등급: {store_all_data.aqi_info.description} (등급: {store_all_data.aqi_info.aqi})
            - 일출시간 : {store_all_data.weatherInfo.sunrise}
            - 일몰시간 : {store_all_data.weatherInfo.sunset}
            - 현재 시간: {store_all_data.format_current_datetime}
            
            작성 가이드 : 
            위 정보를 가진 매장의 오늘 장사지수를 파악해보려고 합니다.
            지역 및 업종, 매출정보, 핵심고객 정보, 날씨 등을 바탕으로 장사지수를 0~100% 사이의 범위에서 추론해주시고
            이유를 45자 이하의 부드러운 서술형으로 작성해주세요.
            ex)오늘의 장사지수 : ??%
            이유...
        """
        content = f"""
            매장명 : {store_all_data.localStoreInfo.store_name}
            주소 : {store_all_data.localStoreInfo.city_name} {store_all_data.localStoreInfo.district_name} {store_all_data.localStoreInfo.sub_district_name}
            업종 : {store_all_data.localStoreInfo.detail_category_name}
            매출이 가장 높은 요일 : {store_all_data.localStoreInfo.commercial_district_max_weekday}
            매출이 가장 높은 시간대 : {store_all_data.localStoreInfo.commercial_district_max_time}
            주 고객층: {store_all_data.localStoreInfo.commercial_district_max_clinet}
            오늘 날짜 : {formatted_date}
            오늘 날씨 : {store_all_data.weatherInfo.main}, {store_all_data.weatherInfo.temp}도, 미세먼지 {store_all_data.aqi_info.description} (등급: {store_all_data.aqi_info.aqi}) 
            현재 시간: {store_all_data.format_current_datetime}

            위 정보를 가진 매장의 오늘 장사지수를 파악해보려고 합니다. 주어진 데이터(지역 및 업종, 매출정보, 핵심고객 정보, 날씨 등)를 바탕으로 아래 양식으로 작성해주세요. 한줄로
            - 오늘의 장사지수 : 0~100% 사이의 범위에서 추론
            - 오늘의 장사지수 이유를 45자 이하의 부드러운 서술형으로 작성해주세요. (오늘의 장사지수 이유 타이틀은 사용하지 않음)
        """

        client = OpenAI(api_key=os.getenv("GPT_KEY"))
        # OpenAI API 키 설정

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": gpt_content},
                {"role": "user", "content": content},
            ],
        )
        report = completion.choices[0].message.content

        # logger.info(f"loc_info_prompt: {content}")
        # logger.info(f"loc_info_gpt: {report}")

        result = GPTAnswer(gpt_answer=report)
        logger.info(f"loc_info_gpt: {result}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service GPTAnswer Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service service_get_store_info_gpt_answer_by_store_info Error: {str(e)}",
        )


def get_daily_operation_tip_gpt_answer(
    store_all_data: LocalStoreInfoWeaterInfoOutput,
) -> GPTAnswer:
    try:
        current_date = datetime.now()
        weekday_map = {
            0: "월요일",
            1: "화요일",
            2: "수요일",
            3: "목요일",
            4: "금요일",
            5: "토요일",
            6: "일요일",
        }
        weekday_name = weekday_map[current_date.weekday()]
        formatted_date = current_date.strftime("%Y-%m-%d")

        holidays = {
            (1, 1): "신정",
            (3, 1): "삼일절",
            (5, 5): "어린이날",
            (6, 6): "현충일",
            (8, 15): "광복절",
            (10, 3): "개천절",
            (10, 9): "한글날",
            (12, 25): "성탄절",
        }
        holiday_instruction = ""
        holiday_name = holidays.get((current_date.month, current_date.day))
        if holiday_name:
            holiday_instruction = f"- 오늘은 대한민국의 {holiday_name}이므로 기념일 분위기를 살린 운영 전략을 먼저 제시해주세요.\n"

        local_info = store_all_data.localStoreInfo
        weather = store_all_data.weatherInfo
        pm = store_all_data.aqi_info

        best_weekday = local_info.commercial_district_max_weekday or ""
        same_weekday_instruction = ""
        if best_weekday and best_weekday == weekday_name:
            same_weekday_instruction = "- 오늘 요일이 가장 매출이 높은 요일과 같으므로, 혼잡한 상황에서 효율적으로 대응할 팁을 포함해주세요.\n"

        best_time = local_info.commercial_district_max_time or "-"
        main_client = local_info.commercial_district_max_clinet or "-"

        content = f"""
당신은 매장 운영 전문 컨설턴트입니다.
당신의 역할은 매장운영이 잘 되는 주요 측면을 식별하고, 아래 매장 데이터의 맥락을 기반으로 운영 지침과 장사에 대한 통찰력을 제공하는 것입니다.
주어진 데이터를 분석하여 아래 양식으로 오늘의 매장운영팁을 작성해주세요.

- 매장 데이터 :
  · 오늘 날씨 : {weather.main}, 기온 {weather.temp}도, 미세먼지 {pm.description}(등급 {pm.aqi})
  · 조회 요일/날짜 : {weekday_name}, {formatted_date}
  · 업종 : {local_info.detail_category_name}
  · 매장주소 : {local_info.city_name} {local_info.district_name} {local_info.sub_district_name}
  · 매장명 : {local_info.store_name}
  · 가장 매출이 높은 요일 : {best_weekday or "-"}
  · 가장 매출이 높은 시간대 : {best_time}
  · 주요 고객 : {main_client}

- 분석 조건 :
  1. 오늘 날짜가 대한민국 기념일이라면 기념일을 우선시하여 매장운영 조언을 해주세요. {holiday_instruction.strip() if holiday_instruction else ""}
  2. 오늘 요일이 가장 매출이 높은 요일과 같다면 손님이 많은 상황에서의 대응 전략을 포함하고, 가장 매출이 높은 시간대와 현재 날씨/기온을 반영한 조언을 해주세요. {same_weekday_instruction.strip() if same_weekday_instruction else ""}
  3. 지역별 특성을 고려하여 지역별 조언을 강조해주세요.
  4. 서술형의 자연스러운 대화체로 모바일 기준 8줄 이상, 10줄 이하로 작성해주세요.
  5. 인삿말을 하지 마세요. 기념일 일때만 기념일관련 언급을 해주세요.
"""
        client = OpenAI(api_key=os.getenv("GPT_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 매장 운영 전문가입니다."},
                {"role": "user", "content": content},
            ],
        )
        report = completion.choices[0].message.content
        return GPTAnswer(gpt_answer=report)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service DailyOperationTip Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service get_daily_operation_tip_gpt_answer Error: {str(e)}",
        )


def get_trend_analysis_gpt_answer(
    store_all_data: LocalStoreInfoWeaterInfoOutput,
) -> GPTAnswer:
    try:
        current_date = datetime.now()
        weekday_map = {
            0: "월요일",
            1: "화요일",
            2: "수요일",
            3: "목요일",
            4: "금요일",
            5: "토요일",
            6: "일요일",
        }
        weekday_name = weekday_map[current_date.weekday()]
        query_month = current_date.strftime("%Y년 %m월")

        local_info = store_all_data.localStoreInfo
        best_weekday = local_info.commercial_district_max_weekday or "-"
        best_time = local_info.commercial_district_max_time or "-"
        main_client = local_info.commercial_district_max_clinet or "-"

        content = f"""
당신은 매장 운영 전문 컨설턴트입니다.
조회 날짜를 기준으로 업종 트렌드를 분석하고 점주에게 조언을 제공해주세요.

ㅇ 매장 데이터 :
- 업종 : {local_info.detail_category_name}
- 매장명 : {local_info.store_name}
- 매장주소 : {local_info.city_name} {local_info.district_name} {local_info.sub_district_name}
- 주요 고객 : {main_client}
- 가장 매출이 높은 요일 : {best_weekday}
- 가장 매출이 높은 시간대 : {best_time}
- 조회 요일 : {weekday_name}
- 조회한 달 : {query_month}

ㅇ 분석 조건 :
- 업종별 트렌드는 계절, 연도, 지역 특성을 고려하여 분석해주세요.
- 오늘 요일이 가장 매출이 높은 요일과 같다면 그 상황을 반영한 조언을 포함해주세요.
- 가장 매출이 높은 시간대, 주요 고객, 지역 특성도 반영해주세요.
- 서술형의 친근한 컨설턴트 말투로 모바일 기준 5줄 이상 길이로 작성하고, '분석'과 '조언'을 구분해 주세요. (예: 분석: ... / 조언: ...)
- 인삿말을 하지 마세요. 기념일 일때만 기념일관련 언급을 해주세요.
"""
        client = OpenAI(api_key=os.getenv("GPT_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 매장 운영 트렌드 분석 전문가입니다."},
                {"role": "user", "content": content},
            ],
        )
        report = completion.choices[0].message.content
        return GPTAnswer(gpt_answer=report)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service TrendAnalysis Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service get_trend_analysis_gpt_answer Error: {str(e)}",
        )


# 뜨는 메뉴 GPT Prompt
def get_rising_business_gpt_answer_by_local_store_top5_menu(
    rising_menu_top5: LocalStoreTop5Menu,
) -> GPTAnswer:

    try:
        city_name = rising_menu_top5.city_name
        district_name = rising_menu_top5.district_name
        sub_district_name = rising_menu_top5.sub_district_name
        detail_category_name = rising_menu_top5.detail_category_name
        region_name = f"{city_name} {district_name} {sub_district_name}"

        top_menu_1 = rising_menu_top5.detail_category_top1_ordered_menu
        top_menu_2 = rising_menu_top5.detail_category_top2_ordered_menu
        top_menu_3 = rising_menu_top5.detail_category_top3_ordered_menu
        top_menu_4 = rising_menu_top5.detail_category_top4_ordered_menu
        top_menu_5 = rising_menu_top5.detail_category_top5_ordered_menu

        content = f"""
            아래 지역 업종의 뜨는 메뉴가 다음과 같습니다. 
            해당 업종의 매장이 고객을 위해 주요 전략으로 가져가야 할 점이 무엇일지 백종원 쉐프 스타일로 조언을 해주세요.
            단, 말투나 전문적 용어는 점주 성향에 맞추고 조언은 4줄 이하로 해주며 두번째줄부터 <br/>으로 한번씩만 줄바꿈을 해줘. 
            - 매장 업종 : {detail_category_name}
            - 매장 위치 : {region_name}
            - 뜨는 메뉴 : 1위 {top_menu_1}, 2위 {top_menu_2}, 3위 {top_menu_3}, 4위 {top_menu_4}, 5위 {top_menu_5}
            - 적용날짜 : {current_time}  {weekday} 
        """

        # logger.info(f"gpt prompt: {content}")

        client = OpenAI(api_key=os.getenv("GPT_KEY"))

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": gpt_content},
                {"role": "user", "content": content},
            ],
        )
        report = completion.choices[0].message.content

        result = GPTAnswer(gpt_answer=report)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service GPTAnswer Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service get_rising_business_gpt_answer_by_local_store_top5_menu Error: {str(e)}",
        )


# 입지 정보 J_Score Gpt Prompt
def get_loc_info_gpt_answer_by_local_store_loc_info(
    loc_data=LocalStoreLocInfoJscoreData,
) -> GPTAnswer:
    try:
        gpt_role = """
            다음과 같은 매장정보 입지 현황을 바탕으로 매장 입지 특징을 분석하시고 입지에 따른 매장운영 가이드를 제시해주세요. 
            각 항목의 점수는 전체 지역 대비 순위를 나타낸것으로 0~10점으로 구성됩니다.
        """
        region_name = f"{loc_data.city_name} {loc_data.district_name} {loc_data.sub_district_name}"

        content = f"""
            다음과 같은 매장정보 입지 현황을 바탕으로 매장 입지 특징을 분석하시고 입지에 따른 매장운영 가이드를 제시해주세요. 
            각 항목의 점수는 전체 지역 대비 순위를 나타낸것으로 0~10점으로 구성됩니다.
            단, 말투나 전문적 용어는 점주 성향에 맞추고 조언은 4줄 이하로 해주며, 두번째줄부터 <br/>으로 한번씩만 줄바꿈을 해줘. 
            매장 정보 입지 현황
            - 매장 업종 : {loc_data.detail_category_name}
            - 매장 위치 : {region_name}
            ###########################
            - 위치 : {region_name}
            - 업종 : {loc_data.detail_category_name}
            - 매장이름 : {loc_data.store_name}
            - 주거인구 수 : {loc_data.loc_info_resident_k * 1000 if loc_data.loc_info_resident_k is not None else "-"} / {loc_data.loc_info_resident_j_score if loc_data.loc_info_resident_j_score is not None else "-"}점
            - 유동인구 수 : {loc_data.loc_info_move_pop_k * 1000 if loc_data.loc_info_move_pop_k is not None else "-"} / {loc_data.loc_info_move_pop_j_score if loc_data.loc_info_move_pop_j_score is not None else "-"}점
            - 업소수 : {loc_data.loc_info_shop_k * 1000 if loc_data.loc_info_shop_k is not None else "-"} / {loc_data.loc_info_shop_j_score if loc_data.loc_info_shop_j_score is not None else "-"}점
            - 지역 평균매출 : {loc_data.loc_info_average_sales_k * 1000 if loc_data.loc_info_average_sales_k is not None else "-"} / {loc_data.loc_info_average_sales_j_score if loc_data.loc_info_average_sales_j_score is not None else "-"}점
            - 월 평균소비 : {loc_data.loc_info_average_spend_k * 1000 if loc_data.loc_info_average_spend_k is not None else "-"} / {loc_data.loc_info_average_spend_j_score if loc_data.loc_info_average_spend_j_score is not None else "-"}점
            - 월 평균소득 : {loc_data.loc_info_income_won * 10000 if loc_data.loc_info_income_won is not None else "-"} / {loc_data.loc_info_income_j_score if loc_data.loc_info_income_j_score is not None else "-"}점
            - 세대 수 : {loc_data.loc_info_house_k * 1000 if loc_data.loc_info_house_k is not None else "-"} / {loc_data.loc_info_house_j_score if loc_data.loc_info_house_j_score is not None else "-"}점
            - 인구 분포 : 10세미만 {loc_data.population_age_10_under}명, 10대 {loc_data.population_age_10s}명, 20대 {loc_data.population_age_20s}명, 30대 {loc_data.population_age_30s}명, 40대 {loc_data.population_age_40s}명, 50대 {loc_data.population_age_50s}명, 60대 {loc_data.population_age_60_over}명, 여성 {round(loc_data.population_female_percent, 1) or 0}% , 남성 {round(loc_data.population_male_percent, 1) or 0}% 

        """
        client = OpenAI(api_key=os.getenv("GPT_KEY"))

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": gpt_content},
                {"role": "user", "content": content},
            ],
        )
        report = completion.choices[0].message.content

        # logger.info(f"loc_info_prompt: {content}")
        # logger.info(f"loc_info_gpt: {report}")

        result = GPTAnswer(gpt_answer=report)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service GPTAnswer Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service get_loc_info_gpt_answer_by_local_store_loc_info Error: {str(e)}",
        )


# 인구 연령별 특성 및 응대방법 GPT
def get_commercial_district_gpt_answer_by_cd_j_score_average(cd_data=LocalStoreLocInfoJscoreData) -> GPTAnswer:
    try:
        gpt_role = """
            위 매장이 위치하는 곳의 업종, 업소수, 평균매출, 평균소득, 평균소비, 유동인구를 분석하고 인구분포를 파악하여 매장에 대한 연령별 특성 및 매출을 높이기 위한 고객 응대방법은 무엇이 있겠습니까? 
            100자 이상, 200자 이하로 개조식으로 작성해주세요.
            """
        # 1️⃣ 연령별 분포 딕셔너리 만들기
        age_distribution = {
            "10세 미만": cd_data.population_age_10_under,
            "10대": cd_data.population_age_10s,
            "20대": cd_data.population_age_20s,
            "30대": cd_data.population_age_30s,
            "40대": cd_data.population_age_40s,
            "50대": cd_data.population_age_50s,
            "60세 이상": cd_data.population_age_60_over,
        }


        # 2️⃣ 가장 높은 2개 나이대 찾기
        sorted_ages = sorted(age_distribution.items(), key=lambda x: x[1], reverse=True)
        top1, top2 = sorted_ages[0][0], sorted_ages[1][0]

        # 3️⃣ 결과 문자열 생성
        content = f"""
            - 매장명 : {cd_data.store_name}
            - 업종 : {cd_data.detail_category_name}
            - 평균 매출 : {cd_data.loc_info_average_sales_k * 1000 if cd_data.loc_info_average_sales_k is not None else "-"}
            - 평균 소득 : {cd_data.loc_info_income_won * 10000 if cd_data.loc_info_income_won is not None else "-"}
            - 평균 소비 : {cd_data.loc_info_average_spend_k * 1000 if cd_data.loc_info_average_spend_k is not None else "-"}
            - 유동 인구 : {cd_data.loc_info_move_pop_k * 1000 if cd_data.loc_info_move_pop_k is not None else "-"}
            - 직장 인구 : {cd_data.loc_info_work_pop_k * 1000 if cd_data.loc_info_work_pop_k is not None else "-"}
            - 인구분포 : 가장 많이 분포연령대 1위: {top1}, 2위: {top2}
        """

        client = OpenAI(api_key=os.getenv("GPT_KEY"))

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": gpt_role},
                {"role": "user", "content": content},
            ],
        )
        report = completion.choices[0].message.content

        # logger.info(f"loc_info_prompt: {content}")
        # logger.info(f"loc_info_gpt: {report}")

        result = GPTAnswer(gpt_answer=report)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service GPTAnswer Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service get_commercial_district_gpt_answer_by_cd_j_score_average Error: {str(e)}",
        )


# 뜨는업종 Gpt Prompt
def get_rising_business_gpt_answer_by_rising_business(
    rising_data=LocalStoreRisingBusinessNTop5SDTop3,
) -> GPTAnswer:
    try:

        content = f"""
                날짜: {rising_data.nice_biz_map_data_ref_date}
                전국 매출 증가 업종 TOP5 
                1위 : {rising_data.rising_business_national_rising_sales_top1_info}%
                2위 : {rising_data.rising_business_national_rising_sales_top2_info}%
                3위 : {rising_data.rising_business_national_rising_sales_top3_info}%
                4위 : {rising_data.rising_business_national_rising_sales_top4_info}%
                5위 : {rising_data.rising_business_national_rising_sales_top5_info}%
                당산2동 매출 증가 업종 Top3
                1위 : {rising_data.rising_business_sub_district_rising_sales_top1_info}
                2위 : {rising_data.rising_business_sub_district_rising_sales_top2_info}
                3위 : {rising_data.rising_business_sub_district_rising_sales_top3_info}
                위 정보를 바탕으로 {rising_data.sub_district_name}에서 {rising_data.detail_category_name} 업종 매장인 {rising_data.store_name} 점포의 영업전략 분석과 조언을 해주세요. 
        """
        client = OpenAI(api_key=os.getenv("GPT_KEY"))

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": gpt_content},
                {"role": "user", "content": content},
            ],
        )
        report = completion.choices[0].message.content

        # logger.info(f"loc_info_prompt: {content}")
        # logger.info(f"loc_info_gpt: {report}")

        result = GPTAnswer(gpt_answer=report)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service GPTAnswer Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service get_rising_business_gpt_answer_by_rising_business Error: {str(e)}",
        )


################ 클로드 결제 후 사용 #################
# import anthropic

# def testCLAUDE():
#     api_key = os.getenv("CLAUDE_KEY")

#     # OpenAI API 키 설정
#     openai.api_key = api_key
#     client = anthropic.Anthropic(
#     api_key={api_key},  # 환경 변수를 설정했다면 생략 가능
#     )

#     message = client.messages.create(
#         model="claude-3-opus-20240229",
#         max_tokens=1000,
#         temperature=0.0,
#         system="Respond only in Yoda-speak.",
#         messages=[
#             {"role": "user", "content": "How are you today?"}
#         ]
#     )

#     print(message.content)


############### 라마 ##################
# import ollama

# def testOLLAMA():
#     response = ollama.chat(model='llama3.1:8b', messages=[
#     {
#         'role': 'user',
#         'content': content,
#     },
#     ])
#     print(response['message']['content'])


if __name__ == "__main__":
    # get_rising_business_gpt_answer_by_local_store_top5_menu("MA0101202212A0017777")

    print("END!!!!!!!!!!!!")
