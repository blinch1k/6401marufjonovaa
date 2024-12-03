from pandas import DataFrame
from pytrends.request import TrendReq
from datetime import date, datetime
import logging

def get_data(keywords : list ,timeframe : str) -> DataFrame:
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, timeframe = timeframe)
    data = pytrends.interest_over_time().drop(columns='isPartial')
    logger = logging.getLogger(__name__)
    logger.info(f"Get dataframe with size {data.size}")
    return data

def get_last_data(keywords : list) -> DataFrame:
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, timeframe = 'now 7-d')
    data = pytrends.interest_over_time().drop(columns='isPartial')
    logger = logging.getLogger(__name__)
    logger.info(f"Get dataframe with size {data.size}")
    return data