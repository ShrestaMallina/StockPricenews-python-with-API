import random
import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid=open("token1.txt","r").read()
auth_token =open("token2.txt","r").read()

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params ={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,

    "apikey":open("stockapi.txt", "r").read(),


}
#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
stock_response = requests.get(url="https://www.alphavantage.co/query",params=stock_params)
stock_response.raise_for_status()
stock_price = stock_response.json()["Time Series (Daily)"]

#yesterday stock closing price
stock_price_list = [value for(key,value) in stock_price.items()]
yesterday_data = stock_price_list[0]
yesterday_closing_price = yesterday_data["4. close"]
# print(yesterday_closing_price)
#daybefore stock closing price
day_before_data = stock_price_list[1]
day_before_closing_price = day_before_data["4. close"]
# print(day_before_closing_price)
#abs difference
difference = float(yesterday_closing_price) - float(day_before_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
# print(difference)
#diff perecentage
diff_percentage = (difference/float(yesterday_closing_price)) * 100
# print(diff_percentage)
if abs(diff_percentage) > 2:
   news_params = {
       "q": COMPANY_NAME,
       "from":"2025-03-25",
       "sortBy":"popularity",
       "apiKey":open("newsapikey.txt","r").read()
   }
   news_api = requests.get(url="https://newsapi.org/v2/everything",params=news_params)
   news_api.raise_for_status()
   data = news_api.json()["articles"]
   three_articles = data[:3]
   three_article = random.choice(three_articles)
   for article in three_article:
       article_headline = article["title"]
       article_brief = article["content"]

       print(article_headline,article_brief)

       client = Client(account_sid, auth_token)
       message = client.messages.create(
           body=f"{STOCK}:{up_down}{round(diff_percentage,0)}%\nHeadline:{article_headline}?\nBrief:{article_brief}",
           from_="+12566022885",
           to= "+919618411774",
       )
       print(message.status)




## STEP 2: Use https://newsapi.org
#https://newsapi.org/v2/everything?q=tesla&from=2025-03-25&sortBy=publishedAt&apiKey=247c928cb87e44aba9290219a65e4e57
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

