import facebook
import dateutil.parser as dateparser
from pylab import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import json

#  here is token which you get from Facebook Graph APIs, every time using program, you need update this token
token = "EAAI386CsZBicBANtKpHpIGDwZC0bvsh3hZAI8P0CrwyToJcf6BneUmY3T6W0gyUTf84qW7sCIWpx6B26Qk9taAqg3LB4w1LDzlXZB7eaYZBroBkrnvHhGz1Fsjt9LhU2oNi6lSmSXxn6phHjSERsrCRAOjbBztKjHmRYLqWYX3OxvX228ZCc0y"
graph = facebook.GraphAPI(token)
# here is a array of post_ids
# The 1st ID is BBC, the 2nd ID is CNN
post_ids = '115664504835242'

page_id = '100091750780759'
post_titles = [
    'TSAofCFB on BBC for article: Obama bans solitary confinement for juveniles',
    'TSAofCFB on CNN for article: Obama bans solitary confinement for juveniles'
]
url = f'https://graph.facebook.com/v16.0/{page_id}_{post_ids}/comments?access_token={token}'

response = requests.request("GET", url)
print(response.text)

# Function get all coments from id-post
def getComments(id_post):
    sentencesComments = []
    timeComments = []
    url = f'https://graph.facebook.com/v16.0/{page_id}_{post_ids}/comments?access_token={token}'

    response = requests.request("GET", url)
    comments = json.loads(response.text)
    #print(comments)

    # comments = graph.get_connections(id=id_post, connection_name='comments', limit = 1000)
    cnt = 0
    for comment in comments['data']:
        try:
            cnt = cnt + 1
            print('Comment {0} : {1} -- Time = {2}'.format(cnt, comment['message'], comment['created_time']))
            sentencesComments.append(comment['message'])
            timeComments.append(comment['created_time'])
        except:
            continue
    return sentencesComments, timeComments


a, b = getComments(115664504835242)

comments, times = getComments(post_ids)

print('Comments:', comments)
print('Times:', times)


def sentimentAnalysis(sentencesComments):
    posY = []
    negY = []
    sid = SentimentIntensityAnalyzer()
    sumPos = 0
    sumNeg = 0
    cnt = 0
    for sentence in sentencesComments:
        cnt += 1
        ss = sid.polarity_scores(sentence)
        for type in sorted(ss):
            if (type == "neg"):
                sumNeg += ss[type]
                negY.append(sumNeg / cnt)
            if (type == "pos"):
                sumPos += ss[type]
                posY.append(sumPos / cnt)
    return posY, negY
postive , negative = sentimentAnalysis(comments)
print("positive " ,postive)
print(negative)