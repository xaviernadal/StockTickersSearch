import requests
import os
import json
import following
import datetime 


tickers = {}

def auth():
    return os.environ.get("BEARER_TOKEN")

def create_url(username):
    query = "from:{} -is:reply -is:retweet".format(username)
    url = "https://api.twitter.com/2/tweets/search/recent?query={}".format(query)
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_ticker(text, username):
    end = [" ", ".", ",", "\n"]
    index = text.find("$")
    ticker = ""
    next_text = text[index::]
    for i in next_text:
        if i in end:
            break
        ticker += i
    text = text.replace(ticker,"")
    ticker = ticker.replace(ticker[1:],ticker[1:].upper())
    if ticker[1:].isalpha():

        count_ticker(ticker, username)
    if "$" in text:
        get_ticker(text, username)

def count_ticker(ticker, username):
    if ticker in tickers.keys():
        ticker_authors = tickers[ticker]
        if username in ticker_authors.keys():
            tickers[ticker][username] += 1
        else:
            tickers[ticker][username] = 1
    else:
        tickers[ticker] = {username: 1}

def print_tickers():
    total = []
    for result in tickers.items():
        ticker = result[0]
        authors = result[1]
        count = 0
        for j in authors.values():
            count += j
        total.append((count,ticker))
    total.sort()
    for element in total:
        print(element[1] + " -> " + str(element[0]))
        print(json.dumps(tickers[element[1]], indent=4))


def main():
    tl = following.main()
    bearer_token = auth()
    for username in tl:
        url = create_url(username)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        if "data" in json_response.keys():
            for tweet in json_response['data']:
                text = tweet["text"]
                if "$" in text:
                    get_ticker(text, username)
                    
    print_tickers()

if __name__ == "__main__":
    main()