import sys, math
#import urllib2
#import urllib.request
import requests
import re
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup



# Download the Key Statistics given a ticker symbol
# Return Key Statistics and list of Keys
def getKeyStats(ticker, DEBUG):
  # Download Key Stats from http://finance.yahoo.com/q/ks?s=MA

  # Open URL
  #  myURL='http://ichart.finance.yahoo.com/table.csv?'+\
  #                       's=%s&d=10&e=20&f=2010&g=d&a=9&b=20&c=2010'%t +\
  #                       '&ignore=.csv'
  #getKeyStatsNew( ticker, DEBUG) ;

  #myURL='http://finance.yahoo.com/q/ks?s=%s'%ticker
  #myURL='http://www.nasdaq.com/symbol/'%ticker
  # myURL='http://www.nasdaq.com/symbol/' + ticker
  myURL='https://www.google.com/finance/quote/MA:NYSE'
  #print "In getKeyStats "
  if (DEBUG ):
      print (myURL)

  #c=urllib2.urlopen(myURL)
  #c = urllib.request.urlopen(myURL)
  c=requests.get(myURL);
  print (c.text) ;

  soup=BeautifulSoup(c.read())
  if DEBUG:
    print (soup)

  #print ("***** soup  ends ***");
  keyCount=0

  key=""
  value=""
  keys={}
  keyStats={}
  keyFlag=True;
  ValueFlag=False;
  for data in soup('div'):
    # Find the div with the class below
    if ('class' in dict(data.attrs) and data['class']=='row overview-results relativeP'):
      if DEBUG:
        print ("*** My My Found div ***")
        print (data)
      for tableCells in data('div'):
         if ('class' in dict(tableCells.attrs) and tableCells['class']=='table-cell'):
          #print ("***  cell ***")
          # print (tableCells.contents)
          # print (tableCells.getText() );
          if ( keyFlag ):
            key=tableCells.getText();
            keys[keyCount]=key
            keyCount=keyCount + 1
            keyFlag=False;
            if DEBUG:
              print ("*** Key is ***")
              print (key)
              print ( len(key) )
          else:
            value=tableCells.getText();
            keyStats[key]=value
            keyFlag=True;
            if DEBUG:
              print ("*** value = ***")
              print (value)
          continue;



  #key=""
  #value=""
  #keys={}
  #keyStats={}
  for td in soup('td'):
  # Prints the heading
    if ('class' in dict(td.attrs) and td['class']=='yfnc_tablehead1'):
      key=td.text
      keys[keyCount]=key
      keyCount=keyCount + 1
      if DEBUG:
        print ("*** Key is ***")
        print (key)

      continue
  # Prints the Value
    if ('class' in dict(td.attrs) and td['class']=='yfnc_tabledata1'):
        value=td.text
        if DEBUG:
          print ("*** value = ***")
          print (value)

        keyStats[key]=value
        #print ("keyStats[key] is " + keyStats[key])
        continue

  # Look for Title
  allDivs=soup.findAll("title");
  for div in allDivs:
    value = div.getText();
    key="title";
    keys[keyCount]=key;
    keyCount=keyCount + 1
    keyStats[key]=value
    #print ()"Title added")

  #Printing keystats
  if DEBUG:
    for k in keyStats:
      print (keyStats[k])
      print (keyCount)

  return keyStats, keyCount


#def getValueFromKey( keyStats, key ):
#  return keyStats[key]


def getValueFromKey( keyStats, key ):
  returnValue="0.0";
  #Check if key exists - Sep 2018
  if ( key in keyStats ):
    returnValue=keyStats[key];
    #print returnValue;
    # Strip out the %
    returnValue=returnValue.replace('%','')
    # Strip out the Commas
    returnValue=returnValue.replace(',','')
    returnValue=returnValue.replace('&nbsp;','')
    returnValue=returnValue.replace('$','')

  return returnValue

#Checks for None and returns Float value
def convertToFloat( dataToConvert ):
  returnValue=dataToConvert;

  if (( returnValue is None )or ( returnValue=="NA" ) or  ( returnValue=="N/A" ) ):
        returnValue=0.0;
  else:
        returnValue=float( returnValue );


  return returnValue

#Sample data is here:
#MA Stock Quote - Mastercard Incorporated Common Stock Price - Nasdaq
#{u"Today's High / Low": u'$&nbsp;218.69&nbsp;/&nbsp;$&nbsp;214.37', u'Forward P/E (1y)': u'33.39'
#, u'Dividend Payment Date': u'8/9/2018', u'1 Year Target': u'225'
#, 'title': u'MA Stock Quote - Mastercard Incorporated Common Stock Price - Nasdaq', u'Previous Close': u'$&nbsp;214.03'
#, u'Market Cap': u'240,871,804,202', u'90 Day Avg. Daily Volume': u'3,132,124', u'Beta': u'1.28', u'P/E Ratio': u'48.7'
#, u'Earnings Per Share (EPS)': u'$&nbsp;4.46', u'Share Volume': u'3,863,896', u'Current Yield': u'0.47 %', u'Ex Dividend Date': u'7/6/2018'
#, u'Annualized Dividend': u'$ 1', u'52 Week High / Low': u'$&nbsp;217.35&nbsp;/&nbsp;$&nbsp;137.75'}

#Set DEBUG=True and run this directly in python. It should be set to False for app engine

DEBUG=True;
ticker="MA"
keyStats , keyCount =getKeyStats(ticker,DEBUG)
eps= getValueFromKey (keyStats,  'Earnings Per Share (EPS)' );

if ( DEBUG ):
  print ("EPS is " + eps) ;
  print (keyStats['title'])
  print (keyStats, keyCount);
