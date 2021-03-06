import json
import os as __os
import requests as __requests
from InstagramAPI import InstagramAPI as __ig
import random as __random
import time as __time
import twitter
from JSONs import *
from caps import *
import moviepy
import facebook

user = ""  # Enter Instagram username
passw = ""  # Add Instagram password

consumer_key = ""  # Add twitter consumer key
consumer_secret = ""  # Add twitter consumer secret key
access_token_key = ""  # Add twitter
access_token_secret = ""  # Add twitter


##For Facebook
user_access_token="" ## Add your (short-lived) user access token.You dont need this if you have a valid long lived token
fb_app_id="" ## Your Facebook App ID
fb_app_secret="" ## Your Facebook app secret
long_lived_token="" ## Add the long-lived access token(If you dont have one don't worry,run the code once and it will provide you with it)
fb_page_id="" ## The page id of the page where you want to post the image to


img = []

curr_dir = __os.path.dirname(__file__)


def check_folder():

    try:
        if not __os.path.exists(__os.path.join(curr_dir, 'red_media')):
            __os.mkdir(__os.path.join(curr_dir, 'red_media'))
            return True
        return True
    except Exception:
        return False


def get_links(__JSON):
    global img
    file = open(__os.path.join(curr_dir, __JSON))
    meme = json.loads(file.read())
    n = meme['data']['dist']

    for i in range(n):
        img.append(meme['data']['children'][i]['data']['preview']['images'][0]['source']['url'])

    print("I got links")
    file.close()


def write_meme():
    global img

    memes = {'data': '[]'}
    memes['data'] = img

    for i in JSONs:
        file = open(f'{i}.txt', 'w+')
        data = json.dumps(memes)
        file.write(data)
        file.close()

    print("Wrote json")


def dload(JSON):
    get_links(JSON)
    write_meme()
    file = open('meme.txt')
    data = file.read()
    data = json.loads(data)

    links = data['data']

    if len(links) == 0:
        print("No links")
    else:

        if check_folder():
            __os.chdir(__os.path.join(curr_dir, 'red_media'))
            i = 0
            print(__os.getcwd())
            for link in links:
                try:
                    print(link)
                    link = link.replace('amp;', '')
                    f = __requests.get(link)

                    m_file = open(__os.path.join(__os.path.dirname(
                        __file__), 'red_media', f'{i}.jpg'), 'wb')

                    for chunk in f.iter_content(100000):
                        m_file.write(chunk)
                    m_file.close()
                    print("Downloaded")
                    __os.chdir('..')
                    i += 1
                except Exception as e:
                    print(e)

        else:
            raise Exception('There has been an error')


def uload(num):
    i = __ig(user, passw)
    i.login()

    a = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret)
    # __os.chdir('\\red_media')

    dirs = __os.listdir(__os.path.join(curr_dir, 'red_media'))

    for j in range(num):
        try:
            files = __random.choice(dirs)
            files = __os.path.join(curr_dir, 'red_media', files)
            i.uploadPhoto(files, caption=__random.choice(cap))
            print("insta upload")
            a.PostUpdate(__random.choice(caps), files)

            print("Uploaded..")
            __os.remove(files)
            __time.sleep(10)
        except Exception as e:
            print("Error occured {}" .format(str(e)))

    i.logout()
    print("Logged out")






def check_user_token():
    try:
        print("checking user access token validity")
        r=__requests.get(url="https://graph.facebook.com/me?access_token="+user_access_token)
        id=r.json()["id"]
        # print(id)
        return True
    except KeyError as k:
        print("Invalid user access token.Your user access token is invalid or has expired.Please refresh your user access tokens through the Graph API Explorer.")
        exit()







def long_access_token(llt,user_access_token,fb_app_id,fb_app_secret):
    try:
        print("checking long lived access token")
        r=__requests.get(url="https://graph.facebook.com/me?access_token="+llt)
        id=r.json()["id"]
        print("success")
    except:
        try:
            print("Invalid long lived token.Your long lived user access token has expired.Exchanging your user access token with a long lived access token")
            print("getting long lived access token")
            r=__requests.get(url="https://graph.facebook.com/v5.0/oauth/access_token?grant_type=fb_exchange_token&client_id="+fb_app_id+"&client_secret="+fb_app_secret+"&fb_exchange_token="+user_access_token)
            llt=r.json()["access_token"]
            print("your long lived access token is :",llt)
            exit()
        except KeyError as k:
            print("unable to get long lived access token")
            check_user_token()








def get_page_access_token(long_lived_token):
    try:
        # print(long_lived_token)
        URL = "https://graph.facebook.com/v5.0/"+fb_page_id+"?fields=access_token&access_token="+long_lived_token
        r= __requests.get(url=URL)
        # print(r.json())
        page_access_token=r.json()["access_token"]
        return page_access_token
    except KeyError as k:
        print("Invalid page access token.Please check your user access tokens")
        exit()







def uload_to_facebook(num):

    # check_user_token()
    long_access_token(long_lived_token,user_access_token,fb_app_id,fb_app_secret)
    page_access_token=get_page_access_token(long_lived_token)
    graph=facebook.GraphAPI(access_token=page_access_token,version="3.0")

    dirs = __os.listdir(__os.path.join(curr_dir, 'red_media'))

    print("facebook upload")
    for j in range(num):
        try:
            files = __random.choice(dirs)
            files = __os.path.join(curr_dir, 'red_media', files)
            photo=open(files,"rb")
            print("posting",files)

            graph.put_photo(
                image=photo,
                message=__random.choice(cap),
            )
            photo.close()
        except Exception as e:
                print("Error occured {}" .format(str(e)))



if __name__ == '__main__':

    if check_folder():
        __os.chdir(__os.path.join(curr_dir, 'red_media'))
        for j in JSONs:
            get_links(j)
            write_meme()
            dload(j)
            uload(input("Enter the number of files to be uploaded: "))
    else:
        print("Error has occured in creating file")
