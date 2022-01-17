import requests
from decouple import config
import json

API_KEY= config('API_KEY')

url = "https://yfapi.net/v6/finance/quote"

# Function to get the data from the Yahoo API's
# result has the json data
def getResults(ticker):
  #querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}
  #querystring = {"symbols":"AAPL"}
  querystring = {"symbols": ticker }

  headers = {
    'x-api-key': API_KEY
    }

  response = requests.request("GET", url, headers=headers, params=querystring)

  print(response.text)

  apiData=json.loads(response.text)

  print (apiData)

  keys=apiData.keys()

  print(keys)

  result=apiData["quoteResponse"]["result"][0]
  resultKeys=result.keys()

  print (result)
  print (resultKeys)

  for x,y in result.items():
    print (x, y)

  print ("Market Price for " + ticker )
  print (result["regularMarketPrice"])

  return result

# Get the value for the given key
def getValueFromResult( result , key):
    value=result[key]
    return value

def getRecommendation( result ):
    recommendation="None"
    forwardPe = getValueFromResult(myResult, "forwardPE")

    if ( forwardPe < 20 ) :
        recommendation="Buy"

    return recommendation


myTicker='AAPL'
myResult=getResults(myTicker)

print( getValueFromResult(myResult, "fiftyTwoWeekHighChangePercent") )
print( getValueFromResult(myResult, "forwardPE") )

print( getRecommendation(myResult) )
