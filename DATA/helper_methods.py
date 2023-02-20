from datetime import datetime, timedelta
import pandas as pd
import random
import requests

#API method to update fx
def getFXs(start_date: datetime, stop_date: datetime, currencyCode: str) -> pd.DataFrame:
    """
    get fx rates from NBP api to PLN. Unfortunately api does not allows more period than 90 days meaning stop - start < 90 days. This returns pandas DataFrame
    """
    #shift to string data
    start_date,stop_date = start_date.strftime("%Y-%m-%d"),stop_date.strftime("%Y-%m-%d")
    url_template = f"http://api.nbp.pl/api/exchangerates/rates/a/{currencyCode}/{start_date}/{stop_date}/"
    request = requests.get(url_template).json()
    df_fx = pd.json_normalize(data=request, record_path='rates')

    return df_fx

def string_date_to_date_time(string_date: str) ->datetime:
    return datetime(int(string_date[:4]), 
                               int(string_date[5:7]),
                               int(string_date[-2:]))

def last_day_of_month(date: datetime) -> datetime:
    thirty = [4,6,9,11]
    thirty_one = [1,3,5,7,8,10,12]
    if (date.month in thirty):
        return datetime(date.year, date.month, 30)
    elif (date.month in thirty_one):
        return datetime(date.year, date.month, 31)
    elif ((date.year % 4 == 0 and date.year % 100 !=0) or (date.year % 400 == 0)):
        return datetime(date.year, date.month, 29)
    else:
        return datetime(date.year, date.month, 28)
    
def random_date_day(year: int,month: int, ):
    max = last_day_of_month(datetime(year,month,1)).day
    #print(max)
    day = random.randint(1,max)
    date=datetime(year,month,day).strftime("%Y-%m-%d")
    return pd.Series([date,day])

def month_number_to_name(x: int):
    dict_month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    return dict_month[x]

def random_weightbased_columnbased(df: pd.DataFrame, column: str):
    x = random.choices(df.index,weights=df[column].values)
    return x[0]
