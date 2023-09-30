import dateutil.parser as dateparser
from pylab import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import json

token = "EAAI386CsZBicBANtKpHpIGDwZC0bvsh3hZAI8P0CrwyToJcf6BneUmY3T6W0gyUTf84qW7sCIWpx6B26Qk9taAqg3LB4w1LDzlXZB7eaYZBroBkrnvHhGz1Fsjt9LhU2oNi6lSmSXxn6phHjSERsrCRAOjbBztKjHmRYLqWYX3OxvX228ZCc0y"

post_ids = '115664504835242'

page_id = '100091750780759'
post_titles = ["review of our facebook page "]

url = f'https://graph.facebook.com/v16.0/{page_id}_{post_ids}/comments?access_token={token}'

response = requests.request("GET", url)
posts = json.loads(response.text)


# Function get all coments from id-post
def getComments(id_post):
    sentencesComments = []
    timeComments = []
    Url = f'https://graph.facebook.com/v16.0/{page_id}_{post_ids}/comments?access_token={token}'

    new_response = requests.request("GET", Url)
    comments = json.loads(new_response.text)

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


# Convert time comment to coordinate X in Graph
def timeToX(x_timeComments, x_created_time_post):
    x_timeX = []
    for timeComment in x_timeComments:
        distTime = dateparser.parse(timeComment) - x_created_time_post
        x = int(distTime.total_seconds())
        x_timeX.append(x)
    return x_timeX


#  Sentiment Analysis comment using NLTK library
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
        for typed in sorted(ss):
            if typed == "neg":
                sumNeg += ss[typed]
                negY.append(sumNeg / cnt)
            if typed == "pos":
                sumPos += ss[typed]
                posY.append(sumPos / cnt)
    return posY, negY


# For each Id_post, we run analysis and create graph temporal sentiment analysis of comments facebook
fi = [plt.figure()] * len(post_ids)
cnt = 0
for post_id in post_ids:
    # Get created time of post
    # created_time_post = dateparser.parse(posts["id"]['created_time'])
    for post in posts['data']:
        created_time_post = dateparser.parse(post['created_time'])
        # do something with created_time_post

    print('Created Time of Post = {0}'.format(created_time_post))
    # Get comment of post
    sentencesComments, timeComments = getComments(post_id)
    # Convert time data
    timeX = timeToX(timeComments, created_time_post)
    # Convert sentiment analysis data
    posY, negY = sentimentAnalysis(sentencesComments)

    # plt.scatter(timeX, posY) #  it will show exactly points if you need
    # plt.scatter(timeX, negY)

    fi[cnt] = plt.figure()
    # fig1 = plt.plot(timeX, posY, color = 'g')
    # fig2 = plt.plot(timeX, negY, color = 'r')
    ax1 = fi[cnt].add_subplot(111)
    ax2 = fi[cnt].add_subplot(111)
    ax1.plot(timeX, posY, color='g')
    ax2.plot(timeX, negY, color='r')

    # Draw annotate of graph
    posYannotate = 20 if posY[0] < 0.5 else -20
    negYannotate = 20 if negY[0] < 0.5 else -20
    index = len(timeX) - 1
    plt.annotate('Positive', xy=(timeX[index], posY[index]), xytext=(40, posYannotate),
                 textcoords='offset points', ha='center', va='bottom',
                 bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',
                                 color='blue'))
    plt.annotate('Negative', xy=(timeX[index], negY[index]), xytext=(40, negYannotate),
                 textcoords='offset points', ha='center', va='bottom',
                 bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',

                                 color='blue'))

    plt.xlabel('Time(s)')
    plt.ylabel('Sentiment analysis')
    fi[0].suptitle(post_titles[0])
    cnt += 1
# Show graph
show()