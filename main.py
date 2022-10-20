import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_url = "https://www.alphavantage.co/query"
stock_api_key = "Y26JNSLAZZ71NIX9"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "interval": "60mins",
    # "outputsize":"compact",
    "apikey": stock_api_key
}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_response = requests.get(url=stock_url, params=parameters)
stock_response.raise_for_status()
stock_price = stock_response.json()
metadata = stock_price["Meta Data"]
daily_stock_data = stock_price["Time Series (Daily)"]

"""parsing the closing values for one day before and the previous days' closing stock price"""

values = [value for key, value in daily_stock_data.items()]
dates = [key for key, value in daily_stock_data.items()]
old_date = dates[3]
new_date = dates[2]
print(old_date, new_date)
yesterday = float(values[2]['4. close'])
day_before_yesterday = float(values[3]['4. close'])

percentage_change = ((day_before_yesterday - yesterday) / day_before_yesterday) * 100

if abs(percentage_change) > 2:
    print(percentage_change)
    print("Get news")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_api_key = "07130f592cc64b0e8d2cb12585806d63"
news_url = "https://newsapi.org/v2/everything?"

news_params = {
    "q": COMPANY_NAME,
    "from": new_date,
    "sortBy": "popularity",
    "pageSize": 3,
    "apikey": news_api_key
}

news_response = requests.get(url=news_url, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()

account_sid = "ACb949dafd8b7bd81aac96ae6a53091656"
auth_token = "71225381a27819232a3b6428cb976fd3"
## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


for i in range(0, 3):
    """Parsing the json response to get the required fields"""
    title = news_data["articles"][i]["title"]
    source = news_data["articles"][i]["source"]["name"]
    description = news_data["articles"][i]["description"]
    url = news_data["articles"][i]["url"]
    # print(f"title: {title}\nDescription {description}\nSource: {source}\nUrl: {url}\n\n")

    if percentage_change < 0:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"Tesla: 🔻{abs(percentage_change)}\nHeadline: {title}\nSource{source}Url: {url}\n\n",
            from_="+17172940573",
            to="+918248005982"
        )
    else:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"Tesla: 🔺{abs(percentage_change)}\nHeadline: {title}\nBrief: {description}\n\n",
            from_="+17172940573",
            to="+918248005982"
        )
# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
