from datetime import datetime
import requests
import pandas as pd


def get_request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("[%s]: Url Request Success" % datetime.datetime.now())
            return response.json()

    except Exception as e:
        print(e)
        print("[%s]: Error for URL : %s" % (datetime.datetime.now(), url))
        return None


# a function that collects a quarterly GDP growth series and future gdp growth

def get_actual_gdp_growth(key, start, end):
    stat_code = '200Y002'
    item_code1 = '10111'

    url = f'http://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/{stat_code}/Q/{start}/{end}/{item_code1}'

    retData = get_request_url(url)

    if (retData == None):
        print("there is no data")
        return None
    else:

        data = retData['StatisticSearch']
        data = pd.DataFrame(data['row'])
        data = data[['DATA_VALUE', 'TIME']]
        data.columns = ['GDP_GROWTH', 'TIME']

        data['DATE'] = pd.to_datetime(data['TIME']).dt.to_period('Q')
        data = data[['GDP_GROWTH', 'DATE']]
        data = data.set_index('DATE')

        size = data.shape[0]

        gdp_series = data.resample('1M', convention='start').pad()
        gdp_series.index = pd.PeriodIndex(gdp_series.index, freq='M')

        return gdp_series


def get_actual_gdp_growth2(key, start, end):
    stat_code = '200Y002'
    item_code1 = '10111'

    url = f'http://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/{stat_code}/Q/{start}/{end}/{item_code1}'

    retData = get_request_url(url)

    if (retData == None):
        print("there is no data")
        return None
    else:

        data = retData['StatisticSearch']
        data = pd.DataFrame(data['row'])
        data = data[['DATA_VALUE', 'TIME']]
        data.columns = ['GDP_GROWTH', 'TIME']

        data['DATE'] = pd.to_datetime(data['TIME']).dt.to_period('Q')
        data = data[['GDP_GROWTH', 'DATE']]
        data = data.set_index('DATE')

        data['GDP_GROWTH_F1'] = data['GDP_GROWTH'].shift(periods=-1)
        data['GDP_GROWTH_F2'] = data['GDP_GROWTH'].shift(periods=-2)
        data['GDP_GROWTH_F3'] = data['GDP_GROWTH'].shift(periods=-3)

        size = data.shape[0]

        gdp_series = data.resample('1M', convention='start').pad()
        gdp_series.index = pd.PeriodIndex(gdp_series.index, freq='M')

        return gdp_series


# a function which collects the individual feature variable

def get_individual_var(access_key, start, end, stat_code, item_code1, item_code2, freq):
    key = access_key

    if item_code2 == 0:
        url = f'http://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/{stat_code}/{freq}/{start}/{end}/{item_code1}'
    else:
        url = f'http://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/{stat_code}/{freq}/{start}/{end}/{item_code1}/{item_code2}'

    retData = get_request_url(url)

    if (retData == None):
        print("there is no data")
        return None

    else:
        data = retData['StatisticSearch']
        data = pd.DataFrame(data['row'])
        return data


start_q = '2001Q1' # whole sample starting point
end_q = '2021Q4'   # whole sample ending point
key = '7MJBDXDXI03KBLP71JFE'
start_m = '201501'
end_m = '202112'
start_m_training = '200101'

simul_data = get_actual_gdp_growth(key, start_q, end_q)
