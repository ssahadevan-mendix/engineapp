import requests
from decouple import config
import json

API_KEY= config('API_KEY')

url = "https://yfapi.net/v6/finance/quote"

#querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}
querystring = {"symbols":"AAPL"}

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
