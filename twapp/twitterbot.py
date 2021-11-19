import tweepy
from decouple import config 

#Extract the auth credentials data from tweepycreds.txt
def show_timeline(instance):
    API_KEY = config("API_KEY")
    API_SECRET_KEY = config("API_SECRET_KEY")
    ACCESS_TOKEN = config("ACCESS_TOKEN")
    SECRET_ACCESS_TOKEN = config("SECRET_ACCESS_TOKEN")

    #authentication to twitter
    auth = tweepy.OAuthHandler(config("API_KEY"), config("API_SECRET_KEY")) 
    auth.set_access_token(config("ACCESS_TOKEN"), config("SECRET_ACCESS_TOKEN"))

    api = tweepy.API(auth)


    user_tweets = api.get_user(screen_name='el_asad_the_don') #@ twitter handle
    for data in user_tweets:
        print(data.screen_name)
        print(data.followers_count)
        for friend in data.friends():
            print(friend.screen_name)

    try:
        api.verify_credentials()
        print("It Lives")

    except:
        print("Something is fishy")