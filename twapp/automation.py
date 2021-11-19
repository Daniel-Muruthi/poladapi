from django.contrib.auth import models
from django.db.models.query import InstanceCheckMeta
from django.http import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import psycopg2
import re
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import string

from twapp.views import TwitterCredsView
from .models import Post, TwitterCreds
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import secrets

@login_required
@receiver(post_save, sender=Post)
def user_tweet(sender, instance, **kwargs):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    driver.get('https://twitter.com/login')
    driver.maximize_window()
    ###############################
    time.sleep(5)
    # if current_user == user
    conn = psycopg2.connect("dbname=polad port=5432 user=moringa password=muruthi1995")
    cur = conn.cursor()
    sor = conn.cursor()
    cur.execute(f"SELECT phone FROM twapp_twittercreds")
    sor.execute(f"SELECT password FROM twapp_twittercreds")
    cred_id= ((Post.get_object(instance.user_id))-1)
    userphone=str(cur.fetchall()[cred_id])
    x=re.sub(r'[' + string.punctuation + ']', '', userphone)
    usercode = str(sor.fetchall()[cred_id])
    y=re.sub(r'[' + string.punctuation + ']', '', usercode)
    ###########################################################
    phone = f'+{x}'
    password = f'{y}'
    tweet = Post.get_absolute_url(instance)

    time.sleep(2)

    loginField = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')

    loginField.send_keys(phone)
    time.sleep(2)

    nextButton =driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div')

    nextButton.click()

    time.sleep(5)

    passwordField = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/label/div/div[2]/div/input')

    passwordField.send_keys(password)
    time.sleep(2)

    loginButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')

    loginButton.click()

    time.sleep(5)


    tweetInputField = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div')

    tweetInputField.send_keys(tweet)

    time.sleep(2)
    tweetButton = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
    driver.execute_script("arguments[0].click();", tweetButton)



