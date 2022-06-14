import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

Stock_APIKey = "TJR1CJJQS7C36MOE"
News_APIKey = "4ad3c524400446f4a54a6277af694804"
Twilio_sid = "AC9a3697c7dd2b3dc61784b808681c6983"
Twilio_auth = "c2351659fbc5385cdabf5a7bd0d6b427"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : Stock_APIKey
}
api = requests.get(STOCK_ENDPOINT, params=api_params)
data = api.json()['Time Series (Daily)']
data_list = [key for (value,key) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

print(yesterday_closing_price)
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage_diff = round((difference/float(yesterday_closing_price)) * 100)
print(percentage_diff)

if abs(percentage_diff) > 5:
    news_params = {
        "apiKey": News_APIKey,
        "q": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    articles_formatted = [f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadline: {article['title']}. \nBrief: {article['description']}"  for article in three_articles]

    client = Client(Twilio_sid, Twilio_auth)
    for article in articles_formatted:
        message = client.messages.create(
            body=article,
            from_="+18575759850",
            to="+919370144677"
        )
