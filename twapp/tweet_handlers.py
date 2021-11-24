import logging
import arrow
import tweepy
import psycopg2
from rest_framework.response import Response
from decouple import config
import re
import string
from twapp.models import ApiCredsModel, Post, TwitterSchedulerModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

############Getting Data From The DB###################

# conn = psycopg2.connect("dbname=tweet port=5432 user=moringa password=muruthi1995")
# ck = conn.cursor()   #consumer key
# at = conn.cursor()   #access token
# cs = conn.cursor()   #consumer secret
# ts = conn.cursor()   #access token secret

# ck.execute(f'SELECT consumer_key FROM twitter_apicredsmodel')
# at.execute(f'SELECT access_token FROM twitter_apicredsmodel')
# cs.execute(f'SELECT consumer_secret FROM twitter_apicredsmodel')
# ts.execute(f'SELECT token_secret FROM twitter_apicredsmodel')

########################################################

############################################################
def get_credentials(pk):

    creds = ApiCredsModel.objects.get(pk=pk)
    owner_creds = ApiCredsModel.objects.filter(user_id=creds.id)
    consumer_key = creds['consumer_key']
    consumer_secret = creds['consumer_secret']
    access_token = creds['access_token']
    access_token_secret = creds['token_secret']

    context={
        "consumer_key":consumer_key,
        "consumer_secret":consumer_secret,
        "access_token":access_token,
        "access_token_secret":access_token_secret,
    }
    return Response(context)

#########################################################


def send_tweets(consumer_key, consumer_secret, access_token,access_token_secret):
    expired_tweets = TwitterSchedulerModel.objects.filter(
    sent=False, tweet_at__lte=arrow.utcnow().datetime)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    if expired_tweets.count() == 0:
        logging.info("No tweet to send as of now")
    for db_tweet in expired_tweets:
        logging.info('sending tweet')
        api.update_status(db_tweet.tweet)
        logging.info('tweet sent')
        db_tweet.sent = True
        db_tweet.save()
# @login_required
# @receiver(post_save, sender=Post)
def tweet_scheduler( **kwargs):
    pk = kwargs.get("pk")
    conn = psycopg2.connect("dbname=polad port=5432 user=moringa password=muruthi1995")
    ck = conn.cursor()   #consumer key
    at = conn.cursor()   #access token
    cs = conn.cursor()   #consumer secret
    ts = conn.cursor()   #access token secret

    ck.execute(f'SELECT consumer_key FROM twapp_apicredsmodel')
    at.execute(f'SELECT access_token FROM twapp_apicredsmodel')
    cs.execute(f'SELECT consumer_secret FROM twapp_apicredsmodel')
    ts.execute(f'SELECT token_secret FROM twapp_apicredsmodel')
    # select consumer_secret from Database where user_id = pk;
    
    con_key=str(ck.fetchall()[pk])
    a=re.sub(r'[' + string.punctuation + ']', '', con_key)
    acc_tok=str(at.fetchall()[pk])
    b=re.sub(r'[' + string.punctuation + ']', '', acc_tok)
    con_sec=str(cs.fetchall()[pk])
    c=re.sub(r'[' + string.punctuation + ']', '', con_sec)
    tok_sec=str(ts.fetchall()[pk])
    d=re.sub(r'[' + string.punctuation + ']', '', tok_sec)


    if (a or b or c or d):
        consumer_key = a
        consumer_secret = b
        access_token = c
        access_token_secret = d
        send_tweets(
            consumer_key, consumer_secret, access_token, access_token_secret)
    else:
        raise NotImplementedError('Lawrence Bot 🤖 says, no credentials found. https://streetgm.gumroad.com/.')
