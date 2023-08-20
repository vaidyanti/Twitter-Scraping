import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
from datetime import date
import pymongo
import json
from PIL import Image

#funtion to scrape data using snscrape
def twitter(username,number):
    tweet_data=[]
    try:
      for i,tweet in enumerate(sntwitter.TwitterSearchScraper('{}'.format(username)).get_items()):
        if i > number :
          break
        else:
          tweet_data.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user,tweet.replyCount, tweet.retweetCount,tweet.lang, tweet.source, tweet.likeCount])
    except:
      pass 
    #creating a dataframe  
    df=pd.DataFrame(tweet_data,columns=['date','id','url','content','user','replyCount','retweetCount','language','source','likeCounts'])
    df['date'] = df['date'].dt.date
    df1=df.loc[(df['date'] >= d1) & (df['date'] <= d2)]
    return df1

#creating two pages of the app
page =st.sidebar.selectbox('Home',['About','Scrape Data'])

#first/home page
if page=='About':
  st.title('Twitter Scraping')
  image = Image.open(r"C:\Users\Administrator\Downloads\scraping-twitter-data-1.png")
  st.image(image)
  st.write("We scrape the data from twitter to get real facts and insights.On this platform you can scrape the data from twitter just by few clicks.")
  image1=Image.open(r"C:\Users\Administrator\Downloads\scrape-twitter.jpg")
  st.write("You can even download the data in semi-structured format in your local pc as csv or json file.")
  st.image(image1)
  st.write('To scrape the data go to the sidebar.')




#secound page where the data is scraped
if page=='Scrape Data':

  st.title('Twitter Scraping')

  a=st.text_input('Enter the Keyword or Hashtag')
  b=st.number_input("Number of Tweets",0,1000)

  d1=st.date_input('Scraped Data From')
  d2=st.date_input('To')

  c=st.button("Display Data")
   
  if c:
      st.dataframe(twitter(a,b))     #calling the funtion

  col1,col2,col3=st.columns(3)
  with col1:
    upload = st.button("Upload Data")
    if upload:                                  #uploading data to mongodb database
      client=pymongo.MongoClient('mongodb+srv://vaidyanti:1234@cluster0.ee0zjto.mongodb.net/?retryWrites=true&w=majority')
      db=client.scraping
      coll=db.tweet
      tweet_dict=twitter(a,b).to_json()
      x={'Scraped Word' : a,'Scraped Date':datetime.datetime.now(),'Scraped Data':tweet_dict}
      coll.insert_one(x)
      st.write("Uploaded Successfully")



  if a and b:
    data1=twitter(a,b).to_json().encode()
    data2=twitter(a,b).to_csv().encode('utf-8')
    #downloading the data as csv and json file
    with col2:
      download1= st.download_button(
        label="Download data as json",
        data=data1,
        file_name='file.json')
    with col3:
      download2=st.download_button(
        label="Download data as csv",
        data=data2,
        file_name='myfile.csv')
