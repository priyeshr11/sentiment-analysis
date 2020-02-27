import requests
import simplekml
import tweepy
import re
from geopy.geocoders import Nominatim

#Create variables for each key, secret, token
consumer_key = 'P5nVNCyNhxs8NuRHzYZcYMpT6'
consumer_secret = 'b3aHobK1PQoctVyAeC8Au6UGbaL56kE1bIj14joVVQTqmpfdL5'
access_token = '781852085407064064-3EVu3pFuWOW4azcFabT1qZF4S6zH7P1'
access_token_secret = '00jr81rcgnSjPNiBj9hBBowjJ1rT6rNth7N8V8ppBr6LO'

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
tapi = tweepy.API(auth)
kml = simplekml.Kml()


        #defining tweets
def tweets(issue):
    search_results = tapi.search(q=issue)
    for tweet in search_results:
        #print(issue, tweet.text.encode('utf8'), tweet.created_at, tweet.user.name, tweet.user.location, tweet.user.followers_count)
        print(tweet.user.name)
        print(tweet.user.location)
    return search_results


        #defining sentiment analysis
def get_sentiment(twt):
    twt = ' '.join(re.sub("(RT@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", twt.text).split())
    result = requests.post("http://text-processing.com/api/sentiment/", data={"text": twt})
    print (twt,result.json()["label"])
    print (twt,result.json()["probability"])
    


        #defining location with kml
def get_coordinates(addr):
    geolocator = Nominatim(user_agent="OpenStreetMap")
    location = geolocator.geocode(addr.user.location)
    if location:
           print((location.latitude, location.longitude))
           pnt = kml.newpoint(name=str(location.raw['display_name']))# display text  
           pnt.coords = [(location.longitude, location.latitude)]    
           pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
           pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/stop.png'
           #icon = {'pos':'grn_circle', 'neg':'red_circle', 'neutral':'wht_circle'}
           kml.save("H:\\My Documents\\Downloads\\tweetfinal.kml") # To save the kml file into computer
   

"""
def write_kml_file(cords, sent, twt):
    pnt = kml.newpoint(name=str(cords.raw['display_name']))# display text  
    pnt.coords = [(cords.longitude, cords.latitude)]    
    pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/stop.png'
    #icon = {'pos':'grn_circle', 'neg':'red_circle', 'neutral':'wht_circle'}
    kml.save("H:\\My Documents\\Downloads\\tweetathome.kml")
    # represent sentiment polarity with icon.  e.g. Red=neg, Green=pos, White=neutral  
    # you can use following code to assign icon for given sentiment where key is the sentiment and value is the icon
"""

def main():
    keyword=input("Please enter the keyword:  ")
    answer=tweets(keyword)
    for tweet in answer:
        #sent=get_sentiment
        #twt=write_kml_file
        get_sentiment(tweet)
        get_coordinates(tweet)
        #write_kml_file(tweet, sent, twt)
    return answer


        
if __name__ == "__main__":
    main()
