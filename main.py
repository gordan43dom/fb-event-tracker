import facebook
from selenium import webdriver
import os
import time
import configparser

config=configparser.ConfigParser()
config.read('config.ini')

event_id = config['DEFAULT']['FB_EVENT_ID']
anchor = "For sale".lower()

graph = facebook.GraphAPI(access_token=config['DEFAULT']['FB_ACCESS_TOKEN'], version=config['DEFAULT']['FB_VER'])

comments = graph.get_object(str(event_id) + '/feed')
last_comment = comments['data'][0]
print(last_comment)

try:
    first_title = last_comment['message']
except KeyError:
    try:
        first_title = last_comment['story']
    except KeyError:
        pass

first_comment_id = last_comment['id']
print(first_title)
index = 1
while True:
    try:
        comments = graph.get_object(str(event_id) + '/feed')
    except ConnectionError:
        print(e)
        continue

    last_comment = comments['data'][0]

    try:
        title = last_comment['message']
    except KeyError:
        try:
            title = last_comment['story']
        except KeyError:
            break;

    if last_comment['id'] == first_comment_id:
        print(str(index) + " : " + title)
        time.sleep(2)
        index += 1
        continue
    else:
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ('1', 400))
        try:
            posts = graph.get_objects(ids=[last_comment['id']], fields='attachments')
        except ConnectionError as e:
            print(e)
            continue
        title = posts[last_comment['id']]['attachments']['data'][0]['target']['url']
        print(title)

        try:
            url = posts[last_comment['id']]['attachments']['data'][0]['target']['url']
            print(url)
            driver = webdriver.Firefox()
            driver.get(url)
        except KeyError:
            print(title)
        first_comment_id = last_comment['id']
        first_title = title
        index = 1
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ('1', 400))
++index



# post = graph.get_object('1152786958109366_1369218289799564/')
# id = '1152786958109366_1369218289799564'
#
#
# print()